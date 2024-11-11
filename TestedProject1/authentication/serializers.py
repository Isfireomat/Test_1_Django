from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class PasswordResetEmailSerializer(serializers.ModelField):
    email = serializers.EmailField()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password"]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['hashed_password'] = make_password(password)
        user: User = User(**validated_data)
        user.save()
        return user