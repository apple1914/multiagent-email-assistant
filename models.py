from pydantic import BaseModel

class UserMessagePayload(BaseModel):
    content: str
    conversation_id: str
