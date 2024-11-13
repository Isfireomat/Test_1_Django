import pytest
from django.conf import settings
from django.db import connections
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse

@pytest.fixture(scope='session')
def db_setup():
    settings.DATABASES['default']['NAME'] = 'test_db'    
    call_command('migrate', interactive=False)
    yield connections['default']


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def standart_user():
    return {'email':'test@gmail.com', 
            'password':'password'}

@pytest.fixture
def standart_link():
    return {'title':"tested",
            'description':"tested",
            'page_url':"https://rabota.by",
            'image':b'picture=',
            'type_url':'website'}

@pytest.fixture
def standart_collection():
    return {
        'title':'test',
        'description':'test'}

@pytest.fixture
def registration(client, standart_user):
    client.post(reverse('registration'), standart_user, format='json')

@pytest.fixture
def user(standart_user, registration):
    user: User = User.objects.get(email=standart_user['email'])
    return user