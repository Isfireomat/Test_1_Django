from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email", "password"]
    
    def create(self, validated_data):
        user: User = User(**validated_data)
        return user