from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
import jwt
from app.database.mongodb import collection_u

from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = "HS256"
security = HTTPBearer()

def generate_jwt_token(data):
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=6)
    payload = {
        'data': data,
        'exp': expiry_time
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return token


def decode_jwt_token(token):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
    if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired, login again"
        )
    return payload['data']


def get_current_user():
    def wrapper(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            data = decode_jwt_token(credentials.credentials)
            user = collection_u.find_one({"id": data.get('id'), "user_type": data.get('user_type')})
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User not found"
                )
            return user
        except HTTPException as e:
            raise e
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired, login again"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or token not found set generated jwt token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    return wrapper