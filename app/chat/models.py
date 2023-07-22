from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from enum import Enum

class MessageStatus(int, Enum):
    SENT = 1
    NOT_SENT = 0

class MessageReturn(BaseModel):
    message_status :str= Field(...,examples=MessageStatus.SENT)
    exception_stats : str = Field(...,examples="Exception Due to")

class Message(BaseModel):
    sender_email:EmailStr=Field(..., example="testing@gmail.com")
    reviever_email:EmailStr=Field(..., example="testing@gmail.com")
    message:str= Field(..., example="This is a demo message")

    