

import time

from fastapi import Depends, HTTPException, Request
from app.config import settings
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.users.models.user import User

# Authentication scheme
oauth2_scheme = HTTPBearer()

def generate_access_token(user_data):
    payload = {
        'user_id': user_data['id'],
        'exp': time.time() + settings.ACCESS_TOKEN_EXPIRES_IN
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def generate_refresh_token(user_data):
    payload = {
        'user_id': user_data['id'],
        'exp': time.time() + settings.REFRESH_TOKEN_EXPIRES_IN
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload['exp'] < time.time():
            raise jwt.ExpiredSignatureError
        # Generate a new access token with the same user_id
        payload['id'] = payload['user_id']
        new_access_token = generate_access_token(payload)
        return new_access_token
    except jwt.ExpiredSignatureError:
        # Handle expired refresh token
        raise Exception("Refresh token has expired.")

def decode_jwt(jwt_token, secret_key):
    try:
        payload = jwt.decode(jwt_token, secret_key, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
    
async def get_current_user(request: Request, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        
        payload = decode_jwt(token.credentials,settings.SECRET_KEY)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Could not validate token")
        # user = User(username=username)
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")