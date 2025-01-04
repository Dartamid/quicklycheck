from django.conf.global_settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core import exceptions
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator,
    NumericPasswordValidator, UserAttributeSimilarityValidator
)
from .exceptions import CustomValidationError
from .models import Account

User = get_user_model()


password_validators = [
    MinimumLengthValidator, NumericPasswordValidator,
]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['user', 'id']


class ProfileSerializer(serializers.ModelSerializer):
    profile = AccountSerializer(read_only=True, source='account')

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'profile']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username']


class TeacherSerializer(serializers.ModelSerializer):
    user_pk = serializers.IntegerField(source='user.pk')
    
    class Meta:
        model = Account
        fields = ['user_pk', 'last_name', 'first_name', 'patronymic']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
    )

    def validate(self, data):
        error = {}
        password = data.get('new_password')
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            error['detail'] = e.messages[0]

        if error:
            raise CustomValidationError(detail=error)

        return super(ChangePasswordSerializer, self).validate(data)


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
        account = Account.objects.create(user=user)
        return user

    def validate_email(self, email):
        if self.Meta.model.objects.filter(email=email).exists():
            raise CustomValidationError(detail={'detail': 'Этот Email уже используется в системе!'})
        return email

    def validate_password(self, password):
        if password is None or password == '':
            raise CustomValidationError(detail={'detail': 'Пароль обязательное поле!'})
        try:
            validate_password(password, self)
            return password
        except ValidationError as e:
            message = e.messages[0]
            raise CustomValidationError(detail={'detail': message})
