from typing import Dict
from users.models import User
from users.serializers import UserSerializer, EmailSerializer

def test_user_serializer_valid() -> None:
    data: Dict[str, str] = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert serializer.is_valid()

def test_user_serializer_email_non_valid() -> None:
    data: Dict[str, str] = {'email': 'testuser', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert not serializer.is_valid()

def test_user_serializer_password_non_valid() -> None:
    data: Dict[str, str] = {'email': 'testuser', 'password': ''}
    serializer: UserSerializer = UserSerializer(data=data)
    assert not serializer.is_valid()

def test_create_user_from_serializer() -> None:
    data: Dict[str, str] = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer: UserSerializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user: User = serializer.create(serializer.validated_data)
    assert user
    assert user.password

def test_password_reset_email_serializer_valid() -> None:
    data: Dict[str, str] = {'email': 'testuser@gmail.com'}
    serializer: EmailSerializer = EmailSerializer(data=data)
    assert serializer.is_valid()

def test_password_reset_email_serializer_email_non_valid() -> None:
    data: Dict[str, str] = {'email': 'testuser'}
    serializer: EmailSerializer = EmailSerializer(data=data)
    assert not serializer.is_valid()