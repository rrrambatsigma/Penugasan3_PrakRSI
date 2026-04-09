from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    user_id: int
    role_id: int
    email: str
    username: str
    password: str

class AccountResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    email: str
    username: str

    class Config:
        from_attributes = True

class AccountPatch(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None