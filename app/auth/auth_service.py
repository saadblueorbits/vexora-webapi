from datetime import datetime
from fastapi import HTTPException,status
from app import utils
from app.auth.dtos.login_user import LoginUserDTO
from app.auth.dtos.register_user import RegisterUserDTO
from app.database import Users
from app.users.models.user import User

class AuthService:


    async def   register_user(self,register_user:RegisterUserDTO):
        existingUser = await Users.find_one({'email':register_user.email})
        if existingUser is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Account Already Exists")
    
        userJSON = register_user.model_dump()
        hashedPassword = utils.hash_password(userJSON['password'])
        userJSON['password'] = hashedPassword
        userJSON['created_on'] = datetime.now()
        userJSON['modified_on'] = datetime.now()
        user = await Users.insert_one(userJSON)
        return {'userId':str(user.inserted_id)}

    async def login_user(self,login_user:LoginUserDTO):
        dbUser = await Users.find_one({"email":login_user.email})
        if dbUser is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found.")
        dbUser['id'] = str(dbUser['_id'])
        user = User(**dbUser)
        flag = utils.verify_password(login_user.password,user.password)
        if flag is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
        return user


authService = AuthService()



