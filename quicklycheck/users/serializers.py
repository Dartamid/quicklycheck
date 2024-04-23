from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .exceptions import CustomValidationError

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'].replace('@', '').replace('.', ''),
            password=validated_data['password']
        )
        return user

    def validate_email(self, email):
        if self.Meta.model.objects.filter(email=email).exists():
            raise CustomValidationError(detail={'detail': 'Этот Email уже используется в системе!'})
        return email


