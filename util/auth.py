import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from config.main import SECRET_KEY, ALGORITHM
from starlette.exceptions import HTTPException
from fastapi import Header


async def create_access_token(data):
    to_encode = {"data": data}
    expire = datetime.utcnow() + timedelta(minutes=180)
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return payload


async def get_token_from_header(authorization: str = Header(None)):
    try:
        assert authorization
    except:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Bad authentication header"},
        )
    return authorization
