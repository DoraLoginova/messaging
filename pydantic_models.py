from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    content: str
