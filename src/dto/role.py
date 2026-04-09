from typing import Optional
from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: str
class RolePatch(BaseModel):
    name: Optional[str] = None