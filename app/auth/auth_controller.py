from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response,status
from app import oauth2
from app.auth.dtos.login_user import LoginUserDTO
from app.auth.dtos.register_user import RegisterUserDTO
from app.auth.auth_service import authService
from app.auth.dtos.verify_email import VerifyEmailDTO
from app.oauth2 import decode_jwt, generate_access_token,generate_refresh_token, refresh_access_token
from app.config import settings
from app.users.models.user import User

router = APIRouter()

@router.post("/register")
async def register(payload:RegisterUserDTO, background_tasks: BackgroundTasks):
    return await authService.register_user(payload,background_tasks)
     

@router.post("/login")
async def login(payload:LoginUserDTO,response: Response):
    resp = await authService.login_user(payload)
    access_token = generate_access_token(resp.model_dump())
    refresh_token = generate_refresh_token(resp.model_dump())
    response.set_cookie('access_token', str(access_token) , settings.ACCESS_TOKEN_EXPIRES_IN * 60,
        settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', str(refresh_token) ,
        settings.REFRESH_TOKEN_EXPIRES_IN * 60, settings.REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', settings.ACCESS_TOKEN_EXPIRES_IN * 60,
        settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}

@router.get("/refresh")
async def refresh_token(request:Request,response:Response):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Please provide refresh token.")
    
    decode_jwt_payload = decode_jwt(refresh_token[2:-1],settings.SECRET_KEY)
    if decode_jwt_payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token.")
    
    access_token = refresh_access_token(refresh_token[2:-1])
    response.set_cookie('access_token', str(access_token) , settings.ACCESS_TOKEN_EXPIRES_IN * 60,
        settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', settings.ACCESS_TOKEN_EXPIRES_IN * 60,
        settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}
        


@router.get('/logout')
def logout(response: Response, user: User = Depends(oauth2.get_current_user)):
    response.set_cookie('logged_in', '', -1)
    response.set_cookie('access_token', '', -1)
    response.set_cookie('refresh_token', '', -1)

    return {'status': 'success'}

@router.post('/verifyemail')
async def verify_email(payload:VerifyEmailDTO):
    await authService.verify_email(payload)
    return {'status':'success'}