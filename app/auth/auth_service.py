from datetime import datetime
import random
from bson import ObjectId
from fastapi import HTTPException,status,BackgroundTasks
from app import smtp, utils
from app.auth.dtos.change_password import ChangePasswordDTO
from app.auth.dtos.forgot_password import ForgotPasswordDTO
from app.auth.dtos.login_user import LoginUserDTO
from app.auth.dtos.recover_password import RecoverPasswordDTO
from app.auth.dtos.register_user import RegisterUserDTO
from app.auth.dtos.verify_email import VerifyEmailDTO
from app.database import Users
from app.users.models.user import User
import uuid


class AuthService:


    async def register_user(self,register_user:RegisterUserDTO, background_tasks: BackgroundTasks):
        try:

            existingUser = await Users.find_one({'email':register_user.email})
            if existingUser is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Account Already Exists")
    
            userJSON = register_user.model_dump()
            hashedPassword = utils.hash_password(userJSON['password'])
            userJSON['password'] = hashedPassword
            userJSON['created_on'] = datetime.now()
            userJSON['modified_on'] = datetime.now()
            userJSON['forgotPasswordToken'] = None
            userJSON['isEmailVerified'] = False 
            userJSON['emailVerificationLinkToken'] = str(uuid.uuid4()) 
            userJSON['emailVerificationCode'] = str(random.randint(1000, 9999)) 
            user = await Users.insert_one(userJSON)
            background_tasks.add_task(smtp.send_email, register_user.email, 'Welcome', 'Welcome To Voxera '+userJSON['emailVerificationLinkToken'] + userJSON['emailVerificationCode'])
            return {'userId':str(user.inserted_id)}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong.")

    async def login_user(self,login_user:LoginUserDTO):
        try:
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
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong.")
    
    async def verify_email(self,verify_email:VerifyEmailDTO):
        try:
            dbUser = await Users.find_one({"emailVerificationLinkToken":verify_email.token})
            if dbUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Token.")
            if dbUser["emailVerificationCode"] != verify_email.code:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Code Is Invalid.")
            dbUser["emailVerificationLinkToken"] = None
            dbUser["emailVerificationCode"] = None
            dbUser["isEmailVerified"] = True
            await Users.update_one({'_id':ObjectId(dbUser['_id'])},{"$set":dbUser},upsert=True)        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong")

    async def forgot_password(self,payload:ForgotPasswordDTO, background_tasks: BackgroundTasks):
        try:
            dbUser = await Users.find_one({'email':payload.email})
            if dbUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found on this email.")
            dbUser["id"] = str(dbUser["_id"])
            user = User(**dbUser)
            user.forgotPasswordToken = str(uuid.uuid4())
            await Users.update_one({'_id':ObjectId(user.id)},{"$set":user.model_dump()},upsert=True)
            background_tasks.add_task(smtp.send_email, user.email, 'Forgot Password', 'Hello '+user.fullName+" here is a token for forgot password : "+user.forgotPasswordToken)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong")
        
    async def recover_password(self,payload:RecoverPasswordDTO):
        try:
            dbUser = await Users.find_one({"forgotPasswordToken":payload.token})
            if dbUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is invalid.")
            dbUser['id'] = str(dbUser['_id']) 
            user = User(**dbUser)
            user.password =  utils.hash_password(payload.password)
            user.forgotPasswordToken = None
            await Users.update_one({'_id':ObjectId(user.id)},{'$set':user.model_dump()},upsert=True)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong")
    
    async def change_password(self,user:User,payload:ChangePasswordDTO):
        try:
            flag = utils.verify_password(payload.oldPassword,user.password)
            if flag is False:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old Password Is Wrong.")
            user.password = utils.hash_password(payload.newPassword)
            await Users.update_one({'_id':ObjectId(user.id)},{'$set':user.model_dump()},upsert=True)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something Went Wrong.")

authService = AuthService()



