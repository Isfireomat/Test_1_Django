import pytest
import binascii
from users.serializers import UserSerializer
from users.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from users.utils import create_token
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.core import mail
import re
from . import client_with_token, standart_user, \
              standart_link_page_url, standart_collection, \
              registration, user, create_link
import json
from rest_framework.response import Response

@pytest.mark.django_db
def test_create_link(client_with_token, standart_link_page_url):
    response = client_with_token.post(reverse('create_link'), 
                                      standart_link_page_url, 
                                      format='json')
    assert response.status_code == 201
    response = client_with_token.post(reverse('create_link'), 
                                      {'url':standart_link_page_url['page_url']}, 
                                      format='json')
    assert response.status_code == 400
    response = client_with_token.post(reverse('create_link'), 
                                      {'page_url':'thelastgame.ru/dwarf-fortress/'}, 
                                      format='json')
    assert response.status_code == 400
    response = client_with_token.post(reverse('create_link'), 
                                      {'page_url':'https://ghgugyigoihgupohpgpui'}, 
                                      format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_read_link(client_with_token, create_link, standart_link_page_url):
    response: Response = client_with_token.post(reverse('read_link'),
                                      {'user_link_id':'1'},
                                      format='json')
    assert response.status_code == 200
    assert standart_link_page_url['page_url'] in \
        response.data.get('link').get('page_url')
    response: Response = client_with_token.post(reverse('read_link'),
                                      {'id':'1'},
                                      format='json')
    assert response.status_code == 400
    response: Response = client_with_token.post(reverse('read_link'),
                                      {'user_link_id':'256'},
                                      format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_link(client_with_token, create_link, standart_link_page_url):
    new_page_url = 'https://thelastgame.ru/factorio/'
    response: Response = client_with_token.post(reverse('update_link'),
                                      {'user_link_id': '1',
                                       'page_url': new_page_url},
                                      format='json')
    assert response.status_code == 201
    assert new_page_url in \
        response.data.get('link').get('page_url')
    assert new_page_url != standart_link_page_url['page_url']
    assert standart_link_page_url['page_url'] not in \
        response.data.get('link').get('page_url')
    
    