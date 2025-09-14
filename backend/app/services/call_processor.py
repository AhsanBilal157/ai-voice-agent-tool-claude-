from .openai_service import OpenAIService
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CallProcessor:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
    
    async def process_transcript(self, transcript: str, driver_name: str, load_number: str) -> Dict[str, Any]:
        """Process call transcript to extract structured data"""
        
        if not self.openai_service or self.openai_service.test_mode:
            logger.info("Processing transcript in test mode")
            # Return dummy structured data for testing
            return {
                "call_outcome": "Test Completed",
                "driver_status": "Driving",
                "current_location": "Highway I-10, near Phoenix",
                "eta": "Tomorrow morning, 9 AM"
            }
        
        system_prompt = f"""You are a call analysis system. Extract structured data from the following call transcript between a dispatch agent and truck driver {driver_name} regarding load {load_number}.

RETURN ONLY valid JSON in this exact format based on the call content:

For regular check-in calls:
{{
    "call_outcome": "In-Transit Update" OR "Arrival Confirmation" OR "Unable to Reach" OR "Incomplete",
    "driver_status": "Driving" OR "Delayed" OR "Arrived" OR "Unknown",
    "current_location": "specific location mentioned or null",
    "eta": "estimated time mentioned or null"
}}

For emergency calls:
{{
    "call_outcome": "Emergency Detected",
    "emergency_type": "Accident" OR "Breakdown" OR "Medical" OR "Other",
    "emergency_location": "specific location mentioned or null",
    "escalation_status": "Escalation Flagged"
}}

If the call was incomplete or the driver was unresponsive:
{{
    "call_outcome": "Unable to Reach" OR "Incomplete",
    "driver_status": "Unresponsive" OR "Unavailable",
    "current_location": null,
    "eta": null
}}

Analyze the following transcript and return ONLY the JSON:"""

        try:
            response = self.openai_service.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                structured_data = json.loads(result)
                return structured_data
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON from OpenAI response: {result}")
                return {
                    "call_outcome": "Processing Error",
                    "driver_status": "Unknown",
                    "current_location": None,
                    "eta": None
                }
                
        except Exception as e:
            logger.error(f"Error processing transcript: {e}")
            return {
                "call_outcome": "Processing Error",
                "driver_status": "Unknown",
                "current_location": None,
                "eta": None
            }