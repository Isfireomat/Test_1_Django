from typing import Dict
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from rest_framework.request import Request
from users.models import User
from users.utils import create_token

def generate_password_reset_link(request: Request, 
                                 user: User) -> Dict[str, str]:
    uid: str = urlsafe_base64_encode(str(user.pk).encode())
    token: str = create_token({'email':user.email}, timedelta(weeks=1))
    reset_link: Dict[str, str] = request.build_absolute_uri(
                                 reverse('password_reset', 
                                 kwargs={'uid': uid, 'token': token})
                                 )
    return reset_link