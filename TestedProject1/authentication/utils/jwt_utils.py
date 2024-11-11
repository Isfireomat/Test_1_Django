import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from authentication.models import User
from typing import Optional, Dict, Any

def create_token(data: Dict[str, Any], 
                expires_delta: Optional[timedelta] = None) -> str:
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + (expires_delta or 
                                                  settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str) -> Optional[Any]:
    try:
        if len(token.split(" ")) == 2:
            token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if not (exp < datetime.now(timezone.utc)): raise jwt.PyJWTError
        return payload
    except jwt.PyJWTError:
        raise Exception("Invalid token")