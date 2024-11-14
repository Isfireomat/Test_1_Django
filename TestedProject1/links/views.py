from datetime import datetime, timedelta, timezone
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Link, Collection
from .serializers import LinkIdSerializer, CollectionIdSerializer,\
                         LinkSerializer, CollectionSerializer
from users.utils import IsAuthenticatedWithToken
import jwt
from django.contrib.auth.hashers import check_password   
from links.utils import get_url_information
from django.db import IntegrityError
from requests.exceptions import HTTPError
from django.core.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_link(request):
    serializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    try:
        url_information: dict = get_url_information(serializer.validated_data['page_url'])
        url_information.update({'user': request.user})
        Link.objects.create(**url_information)
    except Exception as e:
        return Response({'message':'link dont created', 
                         'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'link created'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_link(request):
    serializer = LinkIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                               user=request.user).exists():
        return Response({'Error':'This linc is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    link: Link = Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                                  user=request.user)
    return Response({'link': link.values().first()}, status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_link(request):
    serializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not serializer.validated_data.get('user_link_id'):
        return Response({'message': 'user_link_id is not exists'}, status=status.HTTP_400_BAD_REQUEST)
    if not Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                            user=request.user).exists():
        return Response({'message': 'link is not exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        url_information: dict = get_url_information(serializer.validated_data['page_url'])
        Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                            user=request.user).update(**url_information)
    except Exception as e:
        return Response({'message':'link dont update', 'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    link: Link = Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                                  user=request.user)
    return Response({'message':'link updated', 'link': link.values().first()}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_link(request):
    serializer = LinkIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                               user=request.user).exists():
        return Response({'Error':'This lincs is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                        user= request.user).delete() 
    return Response({'message': 'link deleted'}, status=status.HTTP_200_OK)  

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_collection(request):
    serializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    Collection.objects.create(title=serializer.validated_data['title'],
                              description=serializer.validated_data['description'],
                              user=request.user)
    return Response({'message':'collection created'},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_collection(request):
    serializer = CollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                               user=request.user).exists():
        return Response({'Error':'This collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    collection: Collection = Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                              user=request.user)
    return Response({'collection': collection.values().first()}, status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_collection(request):
    serializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not serializer.validated_data.get('user_collection_id'):
        return Response({'message': 'user_collection_id is not exists'}, status=status.HTTP_400_BAD_REQUEST)
    if not  Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                  user=request.user).exists():
        return Response({'message': 'collection is not exists'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                  user=request.user).update(**serializer.validated_data)
    except Exception as e:
        return Response({'message':'collection dont update', 'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    collection: Collection = Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                              user=request.user)
    return Response({'message':'collection updated', 'collection': collection.values().first()}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_collection(request):
    serializer = CollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                     user=request.user).exists():
        return Response({'Error':'This collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                              user= request.user).delete() 
    return Response({'message': 'collection deleted'}, status=status.HTTP_200_OK) 