from django.contrib.auth import password_validation
from rest_framework import serializers
from checker.models import Class, Student, Test, Pattern, Blank, TempTest, TempPattern, TempBlank
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator,
    NumericPasswordValidator, UserAttributeSimilarityValidator
)
from users.models import User
from django.core import exceptions

password_validators = [
    MinimumLengthValidator, NumericPasswordValidator,
]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['pk', 'number', 'letter', 'created_date']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['pk', 'name', 'grade']


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['pk', 'test', 'num', 'pattern']


class BlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = ['pk', 'test', 'author', 'id_blank', 'var', 'answers']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username']


class TempTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['pk']


class TempPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['pk', 'test', 'num', 'pattern']


class TempBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = ['pk', 'test', 'author', 'id_blank', 'var', 'answers']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
    )

    def validate(self, data):
        errors = dict()
        password = data.get('new_password')
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['detail'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(ChangePasswordSerializer, self).validate(data)

