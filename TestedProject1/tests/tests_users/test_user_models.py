from typing import Dict
from django.core.exceptions import ValidationError
import pytest
from TestedProject1.tests.conftest import client, standart_user, standart_link, standart_collection
from users.models import User

@pytest.mark.django_db
def test_user_model(standart_user: Dict[str, str]) -> None:
    user: User = User.objects.create(email=standart_user['email'],
                                     password=standart_user['password'])
    assert user
    assert user.create_date_time
    assert user.password != standart_user['password']
    old_password: str = user.password
    user.save()
    assert old_password == user.password
    user.set_password("1234567890")
    assert old_password != user.password
    
    
@pytest.mark.django_db
def test_user_model_with_errors(standart_user: Dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        User.objects.create(email='', password=standart_user['password'])
    with pytest.raises(ValidationError):
        User.objects.create(email=standart_user['email'], password='')
    with pytest.raises(ValidationError): 
        User.objects.create(email='test', password=standart_user['password'])