from pydantic import BaseModel
from typing import Optional, Literal

class RegistrationCreate(BaseModel):
    user_id: int
    event_id: int

class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int

    class Config:
        from_attributes = True

class RegistrationPatch(BaseModel):
    status: Optional[Literal["pending", "approved", "rejected"]] = None