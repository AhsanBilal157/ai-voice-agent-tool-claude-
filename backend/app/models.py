# app/models.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class CallTriggerRequest(BaseModel):
    driver_name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=20)
    load_number: str = Field(..., min_length=1, max_length=100)

class ConfigUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    system_prompt: str = Field(..., min_length=10)
    conversation_logic: str = Field(..., min_length=10)

class AgentConfig(BaseModel):
    id: Optional[int] = None
    name: str
    system_prompt: str
    conversation_logic: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CallLog(BaseModel):
    id: Optional[int] = None
    driver_name: str
    phone_number: str
    load_number: str
    call_id: Optional[str] = None
    transcript: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    call_outcome: Optional[str] = None
    created_at: Optional[datetime] = None
    agent_config_id: Optional[int] = None

class StructuredCallData(BaseModel):
    call_outcome: str
    driver_status: Optional[str] = None
    current_location: Optional[str] = None
    eta: Optional[str] = None
    emergency_type: Optional[str] = None
    emergency_location: Optional[str] = None
    escalation_status: Optional[str] = None