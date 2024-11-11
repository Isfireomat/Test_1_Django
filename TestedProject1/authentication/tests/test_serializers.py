from . import client
from authentication.serializers import UserSerializer, PasswordResetEmailSerializer
from authentication.models import User

def test_user_serializer_valid():
    data = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()

def test_user_serializer_email_non_valid():
    data = {'email': 'testuser', 'password': 'password'}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()

def test_user_serializer_password_non_valid():
    data = {'email': 'testuser', 'password': ''}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()

def test_create_user_from_serializer():
    data = {'email': 'testuser@gmail.com', 'password': 'password'}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user: User = serializer.create(serializer.validated_data)
    assert user
    assert user.password

def test_password_reset_email_serializer_valid():
    data = {'email': 'testuser@gmail.com'}
    serializer = PasswordResetEmailSerializer(data=data)
    assert serializer.is_valid()

def test_password_reset_email_serializer_email_non_valid():
    data = {'email': 'testuser'}
    serializer = PasswordResetEmailSerializer(data=data)
    assert not serializer.is_valid()