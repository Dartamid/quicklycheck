from django.conf.global_settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .exceptions import CustomValidationError

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False, max_length=150)
    password = serializers.CharField(
        write_only=True,
        # Проверка через валидатор для ошибки нужного вида
        required=False, allow_blank=True, allow_null=True,
    )

    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        if 'password' not in validated_data.keys():
            raise CustomValidationError(detail={'detail': 'Пароль обязательное поле!'})
        if 'email' not in validated_data.keys():
            raise CustomValidationError(detail={'detail': 'Email обязательное поле!'})
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

    def validate_password(self, password):
        if password is None or password == '':
            raise CustomValidationError(detail={'detail': 'Пароль обязательное поле!'})
        try:
            password_er = validate_password(password, self)
            return password_er
        except ValidationError as e:
            message = e.messages[0]
            raise CustomValidationError(detail={'detail': message})
