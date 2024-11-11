import pytest
from . import client, standart_user
from authentication.serializers import UserSerializer
from authentication.models import User
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_user_model(standart_user):
    user: User = User.objects.create(email=standart_user['email'],
                                     password=standart_user['password'])
    assert user
    assert user.password != standart_user['password']
    old_password: str = user.password
    user.save()
    assert old_password == user.password
    user.set_password("1234567890")
    assert old_password != user.password
    
    
@pytest.mark.django_db
def test_user_model_without_email_password(standart_user):
    try:
        User.objects.create(email='',
                                        password=standart_user['password'])
        assert False
    except Exception as e:
        assert e == ValidationError("Email is required")
    try: 
        User.objects.create(email=standart_user['email'],
                                        password='')
        assert False
    except Exception as e:
        assert e == ValidationError("Password is required")

@pytest.mark.django_db
def test_link_model():
    pass

@pytest.mark.django_db
def test_collection_model():
    pass
