from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import Token
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


# kullanici olusturur ve veritabanina kaydeder.
class RegisterSerializer(serializers.ModelSerializer): #
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None or not user.check_password(data['password']):
            raise serializers.ValidationError("E-posta veya şifre yanlış.")
        return {'user': user}

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs): #gelen veririn dogru formatta oldugunu kontrol eder.
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("Yeni şifreler eşleşmiyor.")
        
        validate_password(attrs['new_password'])
        return attrs

class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            # Access token oluştur
            access_token_payload = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
            }
            access_token = jwt.encode(
                access_token_payload,
                settings.SECRET_KEY,
                algorithm='HS256'
            )

            # Refresh token oluştur
            refresh_token_payload = {
                'user_id': user.id,
                'role': user.role,
                'exp': datetime.utcnow() + timedelta(days=7),
                'iat': datetime.utcnow(),
            }
            refresh_token = jwt.encode(
                refresh_token_payload,
                settings.SECRET_KEY,
                algorithm='HS256'
            )

            return {
                'refresh': refresh_token,
                'access': access_token,
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
            }
        raise serializers.ValidationError("E-posta veya şifre yanlış.")
