from typing import Dict
from datetime import datetime, timezone
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.views import View
import jwt
from users.models import User

class IsAuthenticatedWithToken(BasePermission):
      def has_permission(self, request: Request, view: View) -> bool:
        access_token: str = request.COOKIES.get("access_token")
        if access_token:  
            if not ('Bearer' in access_token): 
                raise AuthenticationFailed("Invalid access token type")
            token: str = access_token.split(" ")[1]    
            try:
                payload: Dict[str, str] = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                if not (payload.get("exp") < datetime.now(timezone.utc).timestamp()): 
                    AuthenticationFailed('Access token has expired')
            except jwt.PyJWTError:
                raise AuthenticationFailed('Invalid access token')
            request.user = User.objects.get(email=payload.get('email'))
            return True
        raise AuthenticationFailed('Invalid tokens')
        