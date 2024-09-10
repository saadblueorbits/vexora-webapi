from bson import ObjectId
from fastapi import HTTPException,status
from app.database import Users
from app.users.models.user import User


class UsersService:

    async def get_by_id(self,userId:str):
        dbUser= await Users.find_one({'_id':ObjectId(userId)})
        if dbUser is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found.')
        dbUser['id'] = str(dbUser['_id']) 
        user = User(**dbUser)
        return user

usersService = UsersService()