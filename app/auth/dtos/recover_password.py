import string
from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class RecoverPasswordDTO(BaseModel):
    token:str
    password:str

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