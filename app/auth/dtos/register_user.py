from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel,EmailStr, Field,field_validator
import string



class RegisterUserDTO(BaseModel):
    email:EmailStr
    phoneNumber: str
    fullName: str
    dob: datetime = Field(
        ...,
        example="1990-01-01",
    )
    password: str

    @field_validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            return False

        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_special_char = any(c not in string.ascii_letters + string.digits for c in password)
        if has_uppercase and has_lowercase and has_number and has_special_char:
            return password
        raise HTTPException(status_code=400,detail='Password Is Weak')
    
    @field_validator('dob')
    def validate_dob(cls, value):
        # Check if the DOB is in the past
        if value >= datetime.today():
            raise HTTPException(status_code=400,detail="Date of birth cannot be in the future.")
        # Add other validation checks as needed (e.g., minimum age, specific date ranges)
        return value

