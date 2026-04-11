from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    whatsapp: str


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class BaseResponse(BaseModel):
    message: str


class RegisterSuccessResponse(BaseResponse):
    data: RegisterResponse