from typing import Dict
import re
from django.conf import settings
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.response import Response
import pytest
from conftest import client, standart_user, standart_link, \
                     standart_collection, registration
from users.models import User
from users.utils import create_token

@pytest.mark.django_db
def test_registration_registration(client: APIClient, 
                                   standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('registration'), 
                                     standart_user, 
                                     format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_registration_with_user_exists(client: APIClient, 
                                            standart_user: Dict[str, str]) -> None:
    client.post(reverse('registration'), standart_user, format='json')
    response: Response = client.post(reverse('registration'), 
                                     standart_user, 
                                     format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_registration_without_valid_data(client: APIClient) -> None:
    response: Response = client.post(reverse('registration'), 
                                     {'email':'tested@gmail.com'}, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_authenticate(client: APIClient, 
                           registration: None, 
                           standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('authenticate'), 
                                     standart_user, format='json')
    assert response.status_code == 200
    assert response.cookies.get('authenticate_token') 

@pytest.mark.django_db
def test_user_authenticate_without_email(client: APIClient, 
                                         registration: None, 
                                         standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('authenticate'), 
                                     {'email':'test', 'password':standart_user['password']}, 
                                     format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_authenticate_without_valid_email(client: APIClient, 
                                               registration: None, 
                                               standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('authenticate'), 
                                     {'email':'test', 'password':standart_user['password']}, 
                                     format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_authenticate_without_email(client: APIClient,
                                         registration: None,
                                         standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('authenticate'), 
                                     {'email':standart_user['email'], 'password':'test'}, 
                                     format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_authenticate_without_email(client: APIClient,
                                         registration: None, 
                                         standart_user: Dict[str, str]):
    response: Response = client.post(reverse('authenticate'), 
                                     {'password':standart_user['password']}, 
                                     format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_tokens(client: APIClient, 
                    registration: None,
                    standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('authenticate'), 
                                     standart_user, format='json')
    client.cookies['authenticate_token'] = response.cookies['authenticate_token']
    response: Response = client.post(reverse('get_tokens'))
    assert response.status_code == 200
    assert 'access_token' in response.data.keys()
    assert 'refresh_token' in response.data.keys()
    assert 'access_token' in response.cookies
    assert 'refresh_token' in response.cookies

@pytest.mark.django_db
def test_get_tokens_without_authenticate_token(client: APIClient,
                                         registration: None) -> None:
    response: Response = client.post(reverse('get_tokens'))
    assert response.status_code == 401
    
@pytest.mark.django_db
def test_refresh_client(client: APIClient, 
                        registration: None) -> None:
    response: Response = client.post(reverse('refresh_token'))
    assert 'access_token' not in response.cookies
    refresh_token: str = create_token({'email':'test@gmail.com'}, 
                                      settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    client.cookies['refresh_token'] = f'Bearer {refresh_token}'
    response: Response = client.post(reverse('refresh_token'))
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    
@pytest.mark.django_db
def test_refresh_client(client: APIClient, 
                        registration: None, 
                        standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('refresh_token'))
    assert 'access_token' not in response.cookies
    refresh_token: Response = create_token({'email':standart_user['email']}, 
                                           settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    client.cookies['refresh_token'] = f'Bearer {refresh_token}'
    response: Response = client.post(reverse('refresh_token'))
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    
@pytest.mark.django_db
def test_change_password(client: APIClient, 
                         registration: None, 
                         standart_user: Dict[str, str]) -> None:
    user: User = User.objects.get(email=standart_user['email'])
    old_password: str = user.password 
    response: Response = client.post(reverse('change_password'), 
                                     {'email':standart_user['email'], 'password':'1234567890'},
                                     format='json')
    assert response.status_code == 403
    response: Response = client.post(reverse('authenticate'), 
                                     standart_user, format='json')
    client.cookies['authenticate_token'] = response.cookies['authenticate_token']
    response: Response = client.post(reverse('get_tokens'), 
                                     {'email':standart_user['email']}, 
                                     format='json')
    client.cookies['access_token'] = response.cookies['access_token']
    response: Response = client.post(reverse('change_password'), 
                                     {'email':standart_user['email'], 'password':''},
                                     format='json')
    assert response.status_code == 400    
    response: Response = client.post(reverse('change_password'), 
                                     {'email':standart_user['email'], 'password':'123456890'},
                                     format='json')
    user: User = User.objects.get(email=standart_user['email'])
    assert response.status_code == 200
    assert old_password != user.password

@pytest.mark.django_db
def test_password_reset_request(client: APIClient, 
                                registration: None, 
                                standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('password_reset_request'),
                                     {'email':standart_user['email']},
                                     form='json')
    assert response.status_code == 200
    assert len(mail.outbox) == 1

@pytest.mark.django_db
def test_password_reset(client: APIClient,
                        registration: None, 
                        standart_user: Dict[str, str]) -> None:
    response: Response = client.post(reverse('password_reset_request'),
                                     {'email':standart_user['email']},
                                     form='json')
    old_password: str = User.objects.get(email=standart_user['email']).password
    assert response.status_code == 200
    assert len(mail.outbox) == 1
    url: str = re.search(r'http[s]?://\S+', mail.outbox[0].body).group(0)
    response: Response = client.post(url, 
                                     {'password':'1234567890'}, 
                                     form='json')
    assert response.status_code == 200
    new_password: str = User.objects.get(email=standart_user['email']).password
    assert old_password != new_password