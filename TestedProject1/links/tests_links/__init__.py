from typing import Generator, Dict
from django.conf import settings
from django.db import connections
from django.core.management import call_command
from django.urls import reverse
from django.db.backends.base.base import BaseDatabaseWrapper
from rest_framework.test import APIClient
import pytest
from users.models import User

@pytest.fixture(scope='session')
def db_setup() -> Generator[BaseDatabaseWrapper, None, None]:
    settings.DATABASES['default']['NAME'] = 'test_db'    
    call_command('migrate', interactive=False)
    yield connections['default']

@pytest.fixture
def client() -> APIClient:
    return APIClient()

@pytest.fixture
def standart_user() -> Dict[str, str]:
    return {'email':'test@gmail.com', 
            'password':'password'}

@pytest.fixture
def standart_link() -> Dict[str, str]:
    return {'title':"tested",
            'description':"tested",
            'page_url':"https://thelastgame.ru/dwarf-fortress/",
            'image':'picture=',
            'type_url':'website'}

@pytest.fixture
def standart_link_page_url() -> Dict[str, str]:
    return {'page_url':"https://thelastgame.ru/dwarf-fortress/"}

@pytest.fixture
def standart_collection() -> Dict[str, str]:
    return {'title':'test',
            'description':"tested"}

@pytest.fixture
def standart_collection() -> Dict[str, str]:
    return {
        'title':'test',
        'description':'test'}

@pytest.fixture
def registration(client: APIClient, standart_user: Dict[str, str]) -> None:
    client.post(reverse('registration'), standart_user, format='json')

@pytest.fixture
def user(standart_user: Dict[str, str], registration: None) -> User:
    user: User = User.objects.get(email=standart_user['email'])
    return user

@pytest.fixture
def client_with_token(client: APIClient, registration: None, standart_user: Dict[str, str]) -> APIClient:
    response = client.post(reverse('get_tokens'), 
                           {'email':standart_user['email']}, format='json')
    client.cookies['access_token'] = response.cookies['access_token']
    return client

@pytest.fixture
def create_link(client_with_token: APIClient, standart_link_page_url: Dict[str, str]) -> None:
    client_with_token.post(reverse('create_link'), 
                           standart_link_page_url, 
                           format='json')

@pytest.fixture
def create_collection(client_with_token: APIClient, standart_collection: Dict[str, str]) -> None:
    response = client_with_token.post(reverse('create_collection'), 
                                      standart_collection, 
                                      format='json')