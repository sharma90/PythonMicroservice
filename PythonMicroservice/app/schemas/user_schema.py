from pydantic import BaseModel, Field
from typing import Optional

# Equivalent to DTO + @Valid

class UserRequest(BaseModel):
    name: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: int
    name: str


    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    success: bool
    data: Optional[UserResponse] = None
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None   

class MessageResponse(BaseModel):
    message: str         