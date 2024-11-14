from typing import Optional, Dict
from datetime import datetime, timezone
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
import jwt
from users.models import User
from users.serializers import UserSerializer, EmailSerializer
from users.utils import create_token, check_token,\
                        IsAuthenticatedWithToken, generate_password_reset_link 

@api_view(['POST'])
def registration(request: Request) -> Response:
    serializer: UserSerializer = UserSerializer(data=request.data)
    if not serializer.is_valid(): 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user: User = serializer.create(serializer.validated_data)
    if User.objects.filter(email=user.email).exists(): 
        return Response({'Error':'This user is not exists'}, status=status.HTTP_400_BAD_REQUEST)
    user.save()
    return Response({'message':'User created'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def authenticate(request: Request) -> Response:
    serializer: UserSerializer = UserSerializer(data=request.data)
    if not serializer.is_valid(): 
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    user: User = serializer.create(serializer.validated_data)
    if not User.objects.filter(email=user.email).exists(): 
        return Response({'Error':'This user is not excists'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    if not check_password(user.password, 
                          User.objects.get(email=user.email).password): 
        return Response({'Error':'Password incorrect'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    authenticate_token: str = create_token({'email': user.email}, 
                                   settings.TEMP_TOKEN_EXPIRE_MINUTES)
    response: Response = Response({'message': 'Authentication successful'}, 
                                  status=status.HTTP_200_OK)
    response.set_cookie(
        key='authenticate_token',
        value=f'Bearer {authenticate_token}',
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=int(settings.TEMP_TOKEN_EXPIRE_MINUTES.total_seconds())
    )
    return response
        
@api_view(['POST'])
def get_tokens(request: Request) -> Response:
    authenticate_token: Optional[str] = request.COOKIES.get('authenticate_token')
    if not authenticate_token or 'Bearer' not in authenticate_token:
        return Response({'message': 'Authentication required'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    authenticate_token: str = authenticate_token.split(' ')[1]
    try:
        payload: Dict[str, str] = jwt.decode(authenticate_token, 
                                             settings.SECRET_KEY, 
                                             algorithms=[settings.ALGORITHM])
        email: str = payload.get('email')
    except jwt.PyJWTError:
        return Response({'message': 'Invalid or expired token'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    access_token: str = create_token({'email':email}, 
                                settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token: str = create_token({'email':email}, 
                                 settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    response: Response = Response({'access_token': access_token,
                                   'refresh_token': refresh_token}, 
                                    status=status.HTTP_200_OK)
    response.set_cookie(
            key='access_token',
            value=f'Bearer {access_token}',
            httponly=True,
            secure=True,
            samesite='lax',
            max_age=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds()))
    response.set_cookie(
            key='refresh_token',
            value=f'Bearer {refresh_token}',
            httponly=True,
            secure=True,
            samesite='lax',
            max_age=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES.total_seconds()))
    return response    

@api_view(['POST'])
def refresh_token(request: Request) -> Response:
    refresh_token: Optional[str] = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'message':'Invalid refresh token'},
                           status=status.HTTP_400_BAD_REQUEST)
    if not ('Bearer' in refresh_token): 
        return Response({'message':'Invalid refresh token type'},
                        status=status.HTTP_400_BAD_REQUEST)
    refresh_token: str = refresh_token.split(' ')[1]    
    try:
        payload: Dict[str, str] = jwt.decode(refresh_token, 
                                             settings.SECRET_KEY, 
                                             algorithms=[settings.ALGORITHM])
        if not (payload.get('exp') < datetime.now(timezone.utc).timestamp()): 
            Response({'message':'Refresh token has expired'},
                        status=status.HTTP_400_BAD_REQUEST)
        new_access_token: str = create_token({'email':payload.get('email')}, 
                                             expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response: Response = Response({'new_access_token': new_access_token,
                                       'resfresh_toke': refresh_token}, 
                                       status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=f'Bearer {new_access_token}',
            httponly=True,
            secure=True,
            samesite='lax',
            max_age=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds()))
        return response
    except jwt.PyJWTError:
        return Response({'message':'Invalid refresh token'},
                        status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def change_password(request: Request) -> Response:
    access_token: Optional[str] = request.COOKIES.get("access_token")
    if not access_token: 
        return Response({'message':'Invalid access token'},
                           status=status.HTTP_400_BAD_REQUEST)
    if not ('Bearer' in access_token): 
        raise Response({'message':'Invalid access token'},
                           status=status.HTTP_400_BAD_REQUEST)
    access_token: str = access_token.split(" ")[1] 
    payload: Dict[str, str] = jwt.decode(access_token, 
                         settings.SECRET_KEY, 
                         algorithms=[settings.ALGORITHM])
    user: User = User.objects.get(email=payload.get('email'))
    if 'password' not in request.data or not request.data['password']: 
        return Response({"message":"Password is not exists"},
                        status=status.HTTP_400_BAD_REQUEST)
    user.set_password(request.data['password'])
    return Response({'message':'Password changed'},
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset_request(request: Request) -> Response:
    serializer: EmailSerializer = EmailSerializer(data=request.data)
    if not serializer.is_valid(): 
         return Response(serializer.errors, 
                         status=status.HTTP_400_BAD_REQUEST)
    try:
        user: User = User.objects.get(email=serializer.validated_data['email'])    
        send_mail("Password Reset Request",
                    f"""Click the link to reset your password: 
                    {generate_password_reset_link(request, user)}\n""",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False)
    except User.DoesNotExist:
        return Response({"message":"User does not exist"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"Email sent"}, 
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset(request: Request, uid: str, token: str) -> Response:
    try:
        uid: str = urlsafe_base64_decode(str(uid)).decode('utf-8')
        user: str = User.objects.get(pk=uid)
        if not check_token(user, token):
            return Response({'message':'Invalid token'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in request.data or not request.data['password']:
            return Response({'message':'Invalid password'},
                            status=status.HTTP_400_BAD_REQUEST) 
        user.set_password(str(request.data['password']))
        return Response({'message':'Password reset'},
                        status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message':'Invalid token'}, 
                        status=status.HTTP_400_BAD_REQUEST)