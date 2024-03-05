from random import randint
from datetime import timedelta
from uuid import uuid4
from fastapi import HTTPException, status
from app.config import settings
from app.repository.userRepository import userRepo
from app.serializers.userSerializers import userEntity, userResponseEntity, getMeResponseEntity
from app.utils.general import exception_message, general_response, hash_password, verify_password
from app.models.users import Users

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


async def register(payload, session):
    def generate_nomor_rekening()->str:
        return '5'+''.join([str(randint(0, 9)) for _ in range(9)])
    try:
        _id = str(uuid4())

        user = await userRepo.findUser(payload.phone_number, payload.nik)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Account already exist')
        user= {}
        user['id'] = _id
        user['nomor_rekening'] = generate_nomor_rekening()
        user['phone_number'] = payload.phone_number
        user['nik'] = payload.nik
        user['pin'] = payload.pin
        user['saldo'] = 0

        await userRepo.create(session, **user)

        data_res = getMeResponseEntity(user)
        data_res.pop("id")

        return await general_response("success", [data_res])

    except Exception as e:
        return exception_message(e)
    
async def login (payload, authorize, response):
    try:
        # Check if the user exist
        db_user = await userRepo.findUserLogin(payload.nomor_rekening, payload.pin)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Your account not found!')
        user = userEntity(db_user)
        # Create access 
        authorize._secret_key = settings.ALGORITHM
        access_token = authorize.create_access_token(
            subject=str(
                user["id"]), expires_time=timedelta(
                minutes=ACCESS_TOKEN_EXPIRES_IN))

        # Create refresh token
        refresh_token = authorize.create_refresh_token(
            subject=str(
                user["id"]), expires_time=timedelta(
                minutes=REFRESH_TOKEN_EXPIRES_IN))

        # We should consider about below code
        # It will set access_token and refresh_token in cookie and it will raise CORS error on some condition
        # Store refresh and access tokens in cookie
        response.set_cookie(
            'access_token',
            access_token,
            ACCESS_TOKEN_EXPIRES_IN * 60,
            ACCESS_TOKEN_EXPIRES_IN * 60,
            '/',
            None,
            False,
            True,
            'lax')
        response.set_cookie(
            'refresh_token',
            refresh_token,
            REFRESH_TOKEN_EXPIRES_IN * 60,
            REFRESH_TOKEN_EXPIRES_IN * 60,
            '/',
            None,
            False,
            True,
            'lax')
        response.set_cookie(
            'logged_in',
            'True',
            ACCESS_TOKEN_EXPIRES_IN * 60,
            ACCESS_TOKEN_EXPIRES_IN * 60,
            '/',
            None,
            False,
            False,
            'lax')
        # Send both access

        # The refresh token must be sent back as well, as it is used to get a
        # new token on the /refresh endpoint
        return {
            'status': 'success',
            'access_token': access_token,
            'refresh_token': refresh_token}
    except Exception as e:
        return exception_message(e)

async def getMe(user_id):
    try:
        tb_users = Users.__tablename__
        user = await userRepo.getById(user_id, tb_users)
        
        data_res = userResponseEntity(user)

        return await general_response("success", {"user":[data_res]})
    except Exception as e:
        return exception_message(e)

async def changePassword(session, payload):
    try:
        data_res = await userRepo.findUser(payload.email)
        print(data_res)
        if not data_res:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email not found!")
        data_res = userEntity(data_res)
        print(data_res)
        if not await verify_password(
                payload.current_password,
                data_res['password']):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Current Password wrong!")

        # Compare password and passwordConfirm
        if payload.password != payload.passwordConfirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Passwords do not match')
        updated_data = payload.dict(exclude_unset=True)

        updated_data.pop("passwordConfirm")
        updated_data.pop("current_password")
        updated_data['password'] = await hash_password(updated_data['password'])
        await userRepo.update(session, data_res['id'], updated_data)
        return {'status': 'success'}
    except Exception as e:
        return exception_message(e)

async def changePin(session, payload):
    try:
        data_res = await userRepo.findUser(payload.nomor_rekening)
        print(data_res)
        if not data_res:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email not found!")
        data_res = userEntity(data_res)
        print(data_res)
        if not await verify_password(
                payload.current_password,
                data_res['password']):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Current Password wrong!")

        # Compare password and passwordConfirm
        if payload.password != payload.passwordConfirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Passwords do not match')
        updated_data = payload.dict(exclude_unset=True)

        updated_data.pop("passwordConfirm")
        updated_data.pop("current_password")
        updated_data['password'] = await hash_password(updated_data['password'])
        await userRepo.update(session, data_res['id'], updated_data)
        return {'status': 'success'}
    except Exception as e:
        return exception_message(e)