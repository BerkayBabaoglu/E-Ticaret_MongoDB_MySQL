# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Dilersen burada şifreyi hashleyebilirsin
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("E-posta bulunamadı.")

        if data['password'] != user.password:
            raise serializers.ValidationError("Şifre hatalı.")

        return {'user': user}
