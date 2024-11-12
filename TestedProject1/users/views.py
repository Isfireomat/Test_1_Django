from datetime import datetime, timedelta, timezone
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, EmailSerializer
from .utils import verify_access_token, create_token, check_token,\
                  IsAuthenticatedWithToken, generate_password_reset_link 
import jwt
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def registration(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid(): 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user: User = serializer.create(serializer.validated_data)
    if User.objects.filter(email=user.email).exists(): return Response({'Error':'This user is excists'}, 
                                                           status=status.HTTP_400_BAD_REQUEST)
    user.save()
    return Response({'message':'User created'}, status=status.HTTP_201_CREATED)

# - Пользователь должен иметь возможность аутентифицироваться
@api_view(['POST'])
def authenticate(request):
    serializer = UserSerializer(data=request.data)
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
    return Response({'message': 'Authentication successful'}, 
                    status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
def get_tokens(request):
    serializer = EmailSerializer(data=request.data)
    if not serializer.is_valid(): 
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    access_token = create_token({'email':request.data['email']}, 
                                settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token({'email':request.data['email']}, 
                                 settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    response: Response = Response({
        'access_token': access_token,
        'refresh_token': refresh_token
    }, status=status.HTTP_200_OK)
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
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'message':'Invalid refresh token'},
                           status=status.HTTP_400_BAD_REQUEST)
    if not ('Bearer' in refresh_token): 
        return Response({'message':'Invalid refresh token type'},
                        status=status.HTTP_400_BAD_REQUEST)
    token = refresh_token.split(' ')[1]    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not (payload.get('exp') < datetime.now(timezone.utc).timestamp()): 
            Response({'message':'Refresh token has expired'},
                        status=status.HTTP_400_BAD_REQUEST)
        new_access_token = create_token({'email':payload.get('email')}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response = Response({'new_access_token': new_access_token,
                                'resfresh_toke': refresh_token
                            }, status=status.HTTP_200_OK)
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
def change_password(request):
    token = request.COOKIES.get("access_token")
    if not token: 
        return Response({'message':'Invalid access token'},
                           status=status.HTTP_400_BAD_REQUEST)
    if not ('Bearer' in token): 
        raise Response({'message':'Invalid access token'},
                           status=status.HTTP_400_BAD_REQUEST)
    token = token.split(" ")[1] 
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user = User.objects.get(email=payload.get('email'))
    if 'password' not in request.data or not request.data['password']: 
        return Response({"message":"Password is not exists"},
                        status=status.HTTP_400_BAD_REQUEST)
    user.set_password(request.data['password'])
    return Response({'message':'Password changed'},
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset_request(request):
    serializer: EmailSerializer = \
        EmailSerializer(data=request.data)
    if not serializer.is_valid(): 
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
def password_reset(request, uid, token):
    try:
        uid = urlsafe_base64_decode(str(uid)).decode('utf-8')
        user = User.objects.get(pk=uid)
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