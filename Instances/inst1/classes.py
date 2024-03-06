from pydantic import BaseModel, EmailStr

class UserLoginSchema(BaseModel):
    user_name: str
    password: str

class UserSchema(BaseModel):
    user_name: str
    email: EmailStr
    password: str

class ResponseMessage:
    succes = ("succes", "test")