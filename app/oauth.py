import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
# from app.repository.userRepository import userRepo
from app.config import settings
# from app.serializers.userSerializers import userResponseEntity

class Settings(BaseModel):
    authjwt_algorithm: str = settings.ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()

def require_user(Authorize: AuthJWT = Depends()) -> dict:
    """checking User valid or not

    Args:
        request (Request): request method
        Authorize (AuthJWT, optional): _description_. Defaults to Depends().

    Raises:
        UserNotFound: if User not found
        NotVerified: if User not verified
        NotUserUser: if User not User
        HTTPException: stattus errr 401 unauthorize

    Returns:
        str: id from database
    """

    try:
        Authorize._secret_key = settings.ALGORITHM
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        return user_id

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Please verify your account')
        if error == 'NotUserUser':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Access rejected!')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid or has expired')
