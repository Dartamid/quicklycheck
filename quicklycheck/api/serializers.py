from django.contrib.auth import password_validation
from rest_framework import serializers
from checker.models import Class, Student, Test, Pattern, Blank, TempTest, TempPattern, TempBlank, Assessment
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator,
    NumericPasswordValidator, UserAttributeSimilarityValidator
)
from users.models import User
from users.exceptions import CustomValidationError
from django.core import exceptions


password_validators = [
    MinimumLengthValidator, NumericPasswordValidator,
]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['pk', 'number', 'letter', 'created_date']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['pk', 'name', 'grade']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade']


class BlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = ['pk', 'test', 'author', 'image', 'id_blank', 'var', 'answers']


class StudentDetailSerializer(serializers.ModelSerializer):
    works = BlankSerializer(many=True, source='works.all')

    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade', 'works']


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['pk', 'test', 'num', 'pattern']


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['pk', 'name', 'color', 'min_pr', 'max_pr']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username']


class TempTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempTest
        fields = ['pk']


class TempPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPattern
        fields = ['pk', 'test', 'num', 'pattern']


class TempBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempBlank
        fields = ['pk', 'test', 'image', 'id_blank', 'var', 'answers']


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
