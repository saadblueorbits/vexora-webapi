from fastapi import APIRouter, Depends
from app.users.dtos.user_resp import UserRespDTO
from app.users.users_service import usersService
from app import oauth2


router = APIRouter()

@router.get('/me')
async def get_me(user_id: str = Depends(oauth2.get_current_user))->UserRespDTO:
    return await usersService.get_by_id(user_id)