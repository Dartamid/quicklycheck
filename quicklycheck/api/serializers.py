from django.contrib.auth import password_validation
from rest_framework import serializers
from checker.models import Class, Student, Test, Pattern, Blank, TempTest, TempPattern, TempBlank, Assessment
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator,
    NumericPasswordValidator, UserAttributeSimilarityValidator
)
from api.teachers.models import User, Account
from api.teachers.exceptions import CustomValidationError
from django.core import exceptions
from api.teachers.serializers import TeacherSerializer
from api.models import Feedback


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade']


class BlankSerializer(serializers.ModelSerializer):
    testName = serializers.CharField(source='test.name', read_only=True)

    class Meta:
        model = Blank
        fields = ['pk', 'test', 'testName', 'author', 'image', 'id_blank', 'var', 'answers']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['pk', 'number', 'letter']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['pk', 'name']


class ClassDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(source='teacher', read_only=True)
    tests = TestSerializer(source='tests.all', many=True, read_only=True)
    students = StudentSerializer(source='students.all', many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['pk', 'number', 'letter', 'teacher', 'tests', 'students']


class StudentDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(source='teacher', read_only=True)
    works = BlankSerializer(many=True, read_only=True, source='works.all')
    grade = ClassSerializer(many=True, read_only=True, source='grade')

    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade', 'teacher', 'works']


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['pk', 'test', 'num', 'pattern']


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['pk', 'name', 'color', 'min_pr', 'max_pr']





class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['pk', 'user', 'text', 'blank']


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



