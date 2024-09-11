from datetime import datetime
import random
from fastapi import HTTPException,status,BackgroundTasks
from app import smtp, utils
from app.auth.dtos.login_user import LoginUserDTO
from app.auth.dtos.register_user import RegisterUserDTO
from app.database import Users
from app.users.models.user import User
import uuid


class AuthService:


    async def register_user(self,register_user:RegisterUserDTO, background_tasks: BackgroundTasks):
        existingUser = await Users.find_one({'email':register_user.email})
        if existingUser is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Account Already Exists")
    
        userJSON = register_user.model_dump()
        hashedPassword = utils.hash_password(userJSON['password'])
        userJSON['password'] = hashedPassword
        userJSON['created_on'] = datetime.now()
        userJSON['modified_on'] = datetime.now()
        userJSON['isEmailVerified'] = False 
        userJSON['emailVerificationLinkToken'] = str(uuid.uuid4()) 
        userJSON['emailVerificationCode'] = str(random.randint(1000, 9999)) 
        user = await Users.insert_one(userJSON)
        background_tasks.add_task(smtp.send_email, register_user.email, 'Welcome', 'Welcome To Voxera '+userJSON['emailVerificationLinkToken'] + userJSON['emailVerificationCode'])
        return {'userId':str(user.inserted_id)}

    async def login_user(self,login_user:LoginUserDTO):
        dbUser = await Users.find_one({"email":login_user.email})
        if dbUser is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found.")
        dbUser['id'] = str(dbUser['_id'])
        user = User(**dbUser)
        if user.isEmailVerified is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please Verify Your Email.")
        flag = utils.verify_password(login_user.password,user.password)
        if flag is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
        return user


authService = AuthService()



