from enum import Enum
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from  typing import Optional
class ChatStatus(str, Enum):
    online = "online"
    offline = "offline"
    busy = "busy"
    dont_disturb = "don't disturb"

class UserStatus(int, Enum):
    active = 1
    disabled = 0

class UserRole(int,Enum):
    admin=0
    regular=1
    
class UserSchema(BaseModel):
    first_name: str = Field(..., example="First name.")
    last_name: str = Field(..., example="Last Name.")
    email: EmailStr = Field(..., example="testing@gmail.com")
    phone_number: Optional[str] = Field(..., example="123456789")
    bio: Optional[str] = Field(..., example="Your bio goes here.")
    chat_status: Optional[str] = Field(..., example=ChatStatus.online)
    user_status: str = Field(..., example=UserStatus.active)
    user_role: Optional[str] = Field(..., example=UserRole.regular)
    profile_picture: Optional[str] = Field(
        ...,
        example="{'preview': 'http://www.example.com/image', 'metaData': 'size, type...'}",
    )
class UserResponse(BaseModel):
    message: str
    user: Optional[UserSchema] = None
