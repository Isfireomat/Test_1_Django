from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt
from users.models import User

def create_token(data: Dict[str, Any], 
                expires_delta: Optional[timedelta] = None) -> str:
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + (expires_delta or 
                                                           settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, settings.SECRET_KEY, 
                      algorithm=settings.ALGORITHM)

def check_token(user: User, token: str) -> bool:
    try:
        payload = jwt.decode(token, 
                             settings.SECRET_KEY, 
                             algorithms=[settings.ALGORITHM])
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if exp < datetime.now(timezone.utc): return False
        if user.email != payload.get('email'): return False
    except jwt.PyJWTError:
        return False
    return True

def verify_access_token(token: str) -> Optional[Any]:
    try:
        if len(token.split(" ")) == 2:
            token = token.split(" ")[1]
        payload = jwt.decode(token, 
                             settings.SECRET_KEY, 
                             algorithms=[settings.ALGORITHM])
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if not (exp < datetime.now(timezone.utc)): raise jwt.PyJWTError
        return payload
    except jwt.PyJWTError:
        raise Exception("Invalid token")