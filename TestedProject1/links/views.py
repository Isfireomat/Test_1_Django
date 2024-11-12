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
from .serializers import IdSerializer, \
                         LinkSerializer, CollectionSerializer
from users.utils import IsAuthenticatedWithToken
import jwt
from django.contrib.auth.hashers import check_password   
   
@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_link(request):
    serializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_link(request):
    serializer = IdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_link(request):
    serializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_link(request):
    serializer = IdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_collection(request):
    serializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_collection(request):
    serializer = IdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_collection(request):
    serializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_collection(request):
    serializer = IdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)