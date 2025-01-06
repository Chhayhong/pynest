from pydantic import BaseModel

class DataOperationMessage(BaseModel):
    detail: str
    
PRIVACY_VALUE_ERROR_MESSAGE = "Privacy must be one of Public or Private"
