import openai
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
            self.test_mode = False
            logger.info("OpenAI service initialized")
        else:
            self.client = None
            self.test_mode = True
            logger.warning("OpenAI API key not provided. Service will run in test mode.")
    
    async def generate_agent_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict], 
        system_prompt: str,
        conversation_logic: str,
        driver_name: str,
        load_number: str
    ) -> str:
        """Generate agent response for real-time conversation"""
        
        if self.test_mode:
            logger.info("Running in test mode - generating dummy response")
            return f"Hello {driver_name}, this is dispatch calling about load {load_number}. How are you doing today?"
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a professional logistics dispatch agent. 

CONTEXT:
- Driver Name: {driver_name}
- Load Number: {load_number}

SYSTEM PROMPT:
{system_prompt}

CONVERSATION LOGIC:
{conversation_logic}

IMPORTANT GUIDELINES:
1. Sound natural and professional
2. If the driver mentions an emergency (accident, breakdown, medical issue, etc.), immediately shift to emergency protocol
3. For emergencies, gather: location, type of emergency, and assure them a human dispatcher will call back
4. For routine check-ins, ask about status, location, and ETA
5. Handle uncooperative or unclear responses professionally
6. Keep responses concise and focused
7. Use natural speech patterns and filler words occasionally to sound human

Emergency keywords to watch for: accident, breakdown, blowout, medical, emergency, help, crash, stuck, problem, issue"""
            }
        ]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": "user" if msg.get("role") == "user" else "assistant",
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Hello {driver_name}, this is dispatch calling about load {load_number}. Can you give me a status update?"
