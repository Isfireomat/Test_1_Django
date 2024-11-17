from django.urls import path
from .views import registration, authenticate, get_tokens, refresh_token, \
                   change_password, password_reset_request, password_reset, email 

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('authenticate/', authenticate, name='authenticate'),
    path('get_tokens/', get_tokens, name='get_tokens'),
    path('refresh_token/', refresh_token, name='refresh_token'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset_request/', password_reset_request, 
         name='password_reset_request'),
    path('password_reset/<str:uid>/<str:token>/', password_reset, name='password_reset'),
    path('email/', email, name='email'),
]