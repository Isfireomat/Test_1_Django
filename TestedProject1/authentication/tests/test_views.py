import pytest
import binascii
from . import client, standart_user, standart_link, standart_collection, \
              registration
from authentication.serializers import UserSerializer
from authentication.models import User, Link, Collection
from django.core.exceptions import ValidationError
from django.urls import reverse

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