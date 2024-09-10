from datetime import datetime
from pydantic import EmailStr
from pydantic_settings import BaseSettings

from app.users.models.user import User

class UserRespDTO(BaseSettings):
    email:EmailStr
    phoneNumber: str
    fullName: str
    dob: datetime
    isEmailVerified:bool
    id:str

    def serializeFromUserEntity(self,user:User):
        self.email = user.email
        self.phoneNumber = user.phoneNumber
        self.dob = user.dob
        self.fullName = user.fullName
        self.id = str(user.id) 
        self.isEmailVerified = user.isEmailVerified