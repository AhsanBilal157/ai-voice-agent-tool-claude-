import aiohttp
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class RetellService:
    def __init__(self, api_key: str, agent_id: str):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = "https://api.retellai.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Check if we have valid credentials
        if not api_key or not agent_id:
            logger.warning("Retell API key or agent ID not provided. Service will run in test mode.")
            self.test_mode = True
        else:
            self.test_mode = False
    
    async def create_call(self, phone_number: str, context: Dict[str, Any], webhook_url: str) -> str:
        """Create a new phone call via Retell AI"""
        
        if self.test_mode:
            logger.info("Running in test mode - simulating call creation")
            # Return a test call ID
            return f"test_call_{hash(phone_number)}"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "agent_id": self.agent_id,
                    "to_number": phone_number,
                    "webhook_url": webhook_url,
                    "metadata": context
                }
                
                logger.info(f"Creating Retell call to {phone_number}")
                
                async with session.post(
                    f"{self.base_url}/create-phone-call",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        call_id = data.get("call_id")
                        logger.info(f"Retell call created successfully: {call_id}")
                        return call_id
                    else:
                        error_text = await response.text()
                        logger.error(f"Retell API error: {response.status} - {error_text}")
                        raise Exception(f"Failed to create call: {error_text}")
        except Exception as e:
            logger.error(f"Error creating Retell call: {e}")
            # Fall back to test mode
            logger.info("Falling back to test mode")
            return f"test_call_{hash(phone_number)}"
