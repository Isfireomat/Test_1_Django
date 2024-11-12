import pytest
import binascii
from . import client, standart_user, standart_link, standart_collection, \
              registration
from authentication.serializers import UserSerializer
from authentication.models import User, Link, Collection
from django.core.exceptions import ValidationError
from django.urls import reverse
from authentication.utils import create_token
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.core import mail
import re

@pytest.mark.django_db
def test_registration_registration(client, standart_user):
    response = client.post(reverse('registration'), standart_user, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_registration_with_user_exists(client, standart_user):
    client.post(reverse('registration'), standart_user, format='json')
    response = client.post(reverse('registration'), standart_user, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_registration_without_valid_data(client, standart_user):
    response = client.post(reverse('registration'), 
                           {'email':'tested@gmail.com'}, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_authenticate(client, registration, standart_user):
    response = client.post(reverse('authenticate'), standart_user, format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_authenticate_without_email(client, registration, standart_user):
    response = client.post(reverse('authenticate'), 
                           {'email':'test', 'password':standart_user['password']}, 
                           format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_authenticate_without_valid_email(client, registration, standart_user):
    response = client.post(reverse('authenticate'), 
                           {'email':'test', 'password':standart_user['password']}, 
                           format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_authenticate_without_email(client, registration, standart_user):
    response = client.post(reverse('authenticate'), 
                           {'email':standart_user['email'], 'password':'test'}, 
                           format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_authenticate_without_email(client, registration, standart_user):
    response = client.post(reverse('authenticate'), 
                           {'password':standart_user['password']}, 
                           format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_tokens(client, registration):
    response = client.post(reverse('get_tokens'), 
                           {'email':'test@gmail.com'}, format='json')
    assert response.status_code == 200
    assert 'access_token' in response.data.keys()
    assert 'refresh_token' in response.data.keys()
    assert 'access_token' in response.cookies
    assert 'refresh_token' in response.cookies

@pytest.mark.django_db
def test_get_tokens_with_non_valid_email(client, registration):
    response = client.post(reverse('get_tokens'), {'email':'test'}, format='json')
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_refresh_client(client, registration):
    response = client.post(reverse('refresh_token'))
    assert 'access_token' not in response.cookies
    refresh_token = create_token({'email':'test@gmail.com'}, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    client.cookies['refresh_token'] = f'Bearer {refresh_token}'
    response = client.post(reverse('refresh_token'))
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    
@pytest.mark.django_db
def test_refresh_client(client, registration, standart_user):
    response = client.post(reverse('refresh_token'))
    assert 'access_token' not in response.cookies
    refresh_token = create_token({'email':standart_user['email']}, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    client.cookies['refresh_token'] = f'Bearer {refresh_token}'
    response = client.post(reverse('refresh_token'))
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    
@pytest.mark.django_db
def test_change_password(client, registration, standart_user):
    user: User = User.objects.get(email=standart_user['email'])
    old_password: str = user.password 
    response = client.post(reverse('change_password'), 
                        {'email':standart_user['email'], 'password':'1234567890'},
                        format='json')
    assert response.status_code == 403
    response = client.post(reverse('get_tokens'), 
                           {'email':standart_user['email']}, format='json')
    client.cookies['access_token'] = response.cookies['access_token']
    response = client.post(reverse('change_password'), 
                           {'email':standart_user['email'], 'password':''},
                           format='json')
    assert response.status_code == 400    
    response = client.post(reverse('change_password'), 
                           {'email':standart_user['email'], 'password':'123456890'},
                           format='json')
    user: User = User.objects.get(email=standart_user['email'])
    assert response.status_code == 200
    assert old_password != user.password
    

@pytest.mark.django_db
def test_password_reset_request(client, registration, standart_user):
    response = client.post(reverse('password_reset_request'),
                           {'email':standart_user['email']},
                           form='json')
    assert response.status_code == 200
    assert len(mail.outbox) == 1

@pytest.mark.django_db
def test_password_reset(client, registration, standart_user):
    response = client.post(reverse('password_reset_request'),
                           {'email':standart_user['email']},
                           form='json')
    old_password: str = User.objects.get(email=standart_user['email']).password
    assert response.status_code == 200
    assert len(mail.outbox) == 1
    url = re.search(r'http[s]?://\S+', mail.outbox[0].body).group(0)
    response = client.post(url, {'password':'1234567890'}, form='json')
    assert response.status_code == 200
    new_password: str = User.objects.get(email=standart_user['email']).password
    assert old_password != new_password