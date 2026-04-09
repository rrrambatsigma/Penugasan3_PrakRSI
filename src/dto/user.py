from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str]
    whatsapp: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    whatsapp: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    whatsapp: str

    class Config:
        from_attributes = True

class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None