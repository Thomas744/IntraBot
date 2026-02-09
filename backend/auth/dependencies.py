from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.auth.auth_utils import decode_access_token
from backend.db.user_repository import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
