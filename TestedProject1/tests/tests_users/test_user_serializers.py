from typing import Dict
from users.models import User
from users.serializers import UserSerializer, EmailSerializer, \
                              PasswordResetSerializer

def test_user_serializer() -> None:
    data: Dict[str, str] = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'email': 'testuser', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'email': 'testuser', 'password': ''}
    serializer: UserSerializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user: User = serializer.create(serializer.validated_data)
    assert user
    assert user.password

def test_email_serializer() -> None:
    data: Dict[str, str] = {'email': 'testuser@gmail.com'}
    serializer: EmailSerializer = EmailSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'email': 'testuser'}
    serializer: EmailSerializer = EmailSerializer(data=data)
    assert not serializer.is_valid()
    
def test_password_reset_serializer() -> None:
    data: Dict[str, str] = {'password': 'password'}
    serializer: PasswordResetSerializer = PasswordResetSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'password': ''}
    serializer: PasswordResetSerializer = PasswordResetSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'passwords': 'password'}
    serializer: PasswordResetSerializer = PasswordResetSerializer(data=data)
    assert not serializer.is_valid()