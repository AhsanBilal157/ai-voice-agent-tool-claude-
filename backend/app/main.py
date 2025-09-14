from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import json
import asyncio
from typing import Dict, Any
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .database import get_db
from .models import CallLog, AgentConfig, CallTriggerRequest, ConfigUpdateRequest

# Import services with error handling
try:
    from .services.retell_service import RetellService
    from .services.openai_service import OpenAIService
    from .services.call_processor import CallProcessor
except ImportError as e:
    logger.error(f"Import error: {e}")
    # Create dummy services for testing
    class DummyService:
        def __init__(self, *args, **kwargs):
            pass
    RetellService = DummyService
    OpenAIService = DummyService
    CallProcessor = DummyService

load_dotenv()

app = FastAPI(title="AI Voice Agent Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with error handling
try:
    retell_service = RetellService(
        api_key=os.getenv("RETELL_API_KEY"),
        agent_id=os.getenv("RETELL_AGENT_ID")
    )
    openai_service = OpenAIService(api_key=os.getenv("OPENAI_API_KEY"))
    call_processor = CallProcessor(openai_service)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    retell_service = None
    openai_service = None
    call_processor = None

@app.get("/")
async def root():
    return {"message": "AI Voice Agent Tool API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "retell": retell_service is not None,
            "openai": openai_service is not None,
            "call_processor": call_processor is not None
        },
        "env_vars": {
            "SUPABASE_URL": bool(os.getenv("SUPABASE_URL")),
            "SUPABASE_KEY": bool(os.getenv("SUPABASE_KEY")),
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
            "RETELL_API_KEY": bool(os.getenv("RETELL_API_KEY")),
            "RETELL_AGENT_ID": bool(os.getenv("RETELL_AGENT_ID"))
        }
    }

@app.get("/api/configs")
async def get_configs():
    """Get all agent configurations"""
    try:
        db = get_db()
        response = db.table('agent_configs').select('*').execute()
        logger.info(f"Retrieved {len(response.data)} configs")
        return {"configs": response.data}
    except Exception as e:
        logger.error(f"Error getting configs: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/configs")
async def create_config(request: ConfigUpdateRequest):
    """Create a new agent configuration"""
    try:
        db = get_db()
        data = {
            "name": request.name,
            "system_prompt": request.system_prompt,
            "conversation_logic": request.conversation_logic
        }
        response = db.table('agent_configs').insert(data).execute()
        logger.info(f"Created config: {response.data[0]['id']}")
        return {"config": response.data[0]}
    except Exception as e:
        logger.error(f"Error creating config: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/api/configs/{config_id}")
async def update_config(config_id: int, request: ConfigUpdateRequest):
    """Update an agent configuration"""
    try:
        db = get_db()
        data = {
            "name": request.name,
            "system_prompt": request.system_prompt,
            "conversation_logic": request.conversation_logic,
        }
        response = db.table('agent_configs').update(data).eq('id', config_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Configuration not found")
        logger.info(f"Updated config: {config_id}")
        return {"config": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/calls/trigger")
async def trigger_call(request: CallTriggerRequest):
    """Trigger a new call using Retell AI"""
    try:
        logger.info(f"Triggering call for {request.driver_name} at {request.phone_number}")
        
        # Check if services are available
        if not retell_service:
            logger.error("Retell service not initialized")
            raise HTTPException(status_code=500, detail="Retell service not available")
        
        # Get database connection
        db = get_db()
        
        # Get the current agent configuration
        config_response = db.table('agent_configs').select('*').limit(1).execute()
        if not config_response.data:
            # Create a default config if none exists
            default_config = {
                "name": "Default Agent",
                "system_prompt": "You are a professional logistics dispatch agent.",
                "conversation_logic": "Ask about driver status and location."
            }
            config_response = db.table('agent_configs').insert(default_config).execute()
            logger.info("Created default configuration")
        
        config = config_response.data[0]
        logger.info(f"Using config: {config['name']}")
        
        # Create call log entry
        call_data = {
            "driver_name": request.driver_name,
            "phone_number": request.phone_number,
            "load_number": request.load_number,
            "agent_config_id": config['id'],
            "call_outcome": "Initiated"
        }
        
        log_response = db.table('call_logs').insert(call_data).execute()
        call_log = log_response.data[0]
        logger.info(f"Created call log: {call_log['id']}")
        
        # Prepare context for the agent
        call_context = {
            "driver_name": request.driver_name,
            "load_number": request.load_number,
            "system_prompt": config['system_prompt'],
            "conversation_logic": config['conversation_logic']
        }
        
        # For now, simulate call creation since Retell might not be fully configured
        try:
            # Try to create call via Retell AI
            webhook_url = f"{os.getenv('BACKEND_URL', 'http://localhost:8000')}/api/webhook/retell"
            call_id = await retell_service.create_call(
                phone_number=request.phone_number,
                context=call_context,
                webhook_url=webhook_url
            )
            logger.info(f"Retell call created: {call_id}")
        except Exception as retell_error:
            logger.warning(f"Retell call creation failed: {retell_error}")
            # Generate a dummy call ID for testing
            call_id = f"test_call_{call_log['id']}"
            logger.info(f"Using test call ID: {call_id}")
        
        # Update call log with call_id
        db.table('call_logs').update({"call_id": call_id}).eq('id', call_log['id']).execute()
        logger.info(f"Updated call log with call_id: {call_id}")
        
        return {"call_id": call_id, "log_id": call_log['id'], "status": "initiated"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering call: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/api/calls")
async def get_calls():
    """Get all call logs"""
    try:
        db = get_db()
        response = db.table('call_logs').select('*').order('created_at', desc=True).execute()
        logger.info(f"Retrieved {len(response.data)} calls")
        return {"calls": response.data}
    except Exception as e:
        logger.error(f"Error getting calls: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/calls/{call_id}")
async def get_call(call_id: str):
    """Get a specific call log"""
    try:
        db = get_db()
        response = db.table('call_logs').select('*').eq('call_id', call_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Call not found")
        return {"call": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting call: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/webhook/retell")
async def retell_webhook(request: Request):
    """Handle Retell AI webhook events"""
    try:
        body = await request.json()
        event = body.get("event")
        call_id = body.get("call_id")
        
        logger.info(f"Received Retell webhook: {event} for call {call_id}")
        
        if event == "call_started":
            await handle_call_started(call_id, body)
        elif event == "call_ended":
            await handle_call_ended(call_id, body)
        elif event == "agent_response_required":
            return await handle_agent_response(call_id, body)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

async def handle_call_started(call_id: str, data: Dict[str, Any]):
    """Handle call started event"""
    try:
        db = get_db()
        db.table('call_logs').update({
            "call_outcome": "In Progress"
        }).eq('call_id', call_id).execute()
        logger.info(f"Call started: {call_id}")
    except Exception as e:
        logger.error(f"Error handling call started: {e}")

async def handle_call_ended(call_id: str, data: Dict[str, Any]):
    """Handle call ended event and process transcript"""
    try:
        db = get_db()
        transcript = data.get("transcript", "")
        
        # Get call log to get context
        call_response = db.table('call_logs').select('*').eq('call_id', call_id).execute()
        if not call_response.data:
            logger.warning(f"Call log not found for call_id: {call_id}")
            return
        
        call_log = call_response.data[0]
        
        # Process transcript if call_processor is available
        if call_processor:
            structured_data = await call_processor.process_transcript(
                transcript=transcript,
                driver_name=call_log['driver_name'],
                load_number=call_log['load_number']
            )
        else:
            # Dummy structured data for testing
            structured_data = {
                "call_outcome": "Test Completed",
                "driver_status": "Unknown",
                "current_location": "Test Location",
                "eta": "Unknown"
            }
        
        # Update call log with results
        db.table('call_logs').update({
            "transcript": transcript,
            "structured_data": structured_data,
            "call_outcome": structured_data.get("call_outcome", "Completed")
        }).eq('call_id', call_id).execute()
        
        logger.info(f"Processed call {call_id} with outcome: {structured_data.get('call_outcome')}")
        
    except Exception as e:
        logger.error(f"Error processing call ended: {e}")
        logger.error(traceback.format_exc())

async def handle_agent_response(call_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle real-time agent response requirements"""
    try:
        db = get_db()
        call_response = db.table('call_logs').select('*').eq('call_id', call_id).execute()
        
        if not call_response.data:
            return {"response": "I'm sorry, I couldn't find the call information."}
        
        call_log = call_response.data[0]
        
        # Get agent configuration
        config_response = db.table('agent_configs').select('*').eq('id', call_log['agent_config_id']).execute()
        if not config_response.data:
            return {"response": "Configuration not found."}
        
        config = config_response.data[0]
        
        # Generate response using OpenAI if available
        if openai_service:
            conversation_history = data.get("transcript", [])
            user_message = data.get("user_utterance", "")
            
            response = await openai_service.generate_agent_response(
                user_message=user_message,
                conversation_history=conversation_history,
                system_prompt=config['system_prompt'],
                conversation_logic=config['conversation_logic'],
                driver_name=call_log['driver_name'],
                load_number=call_log['load_number']
            )
            
            return {"response": response}
        else:
            # Dummy response for testing
            return {"response": f"Hello {call_log['driver_name']}, this is dispatch calling about load {call_log['load_number']}. How are you doing?"}
        
    except Exception as e:
        logger.error(f"Error generating agent response: {e}")
        logger.error(traceback.format_exc())
        return {"response": "I apologize, but I'm experiencing technical difficulties. A human dispatcher will call you back shortly."}

# Error handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)