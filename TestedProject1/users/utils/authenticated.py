from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta, timezone
from .jwt_utils import create_token
from users.models import User
import jwt

class IsAuthenticatedWithToken(BasePermission):
      def has_permission(self, request, view):
        access_token = request.COOKIES.get("access_token")
        if access_token:  
            if not ('Bearer' in access_token): 
                raise AuthenticationFailed("Invalid access token type")
            token = access_token.split(" ")[1]    
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                if not (payload.get("exp") < datetime.now(timezone.utc).timestamp()): 
                    AuthenticationFailed('Access token has expired')
            except jwt.PyJWTError:
                raise AuthenticationFailed('Invalid access token')
            request.user = User.objects.get(email=payload.get('email'))
            return True
        raise AuthenticationFailed('Invalid tokens')
        