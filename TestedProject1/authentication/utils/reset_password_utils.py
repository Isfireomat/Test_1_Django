from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def generate_password_reset_link(request, user):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(
                        reverse('password_reset', 
                                 kwargs={'uid': uid, 'token': token}))
    return reset_link