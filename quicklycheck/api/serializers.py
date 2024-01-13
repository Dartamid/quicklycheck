from rest_framework import serializers
from checker.models import Class, Student, Test, Pattern, Blank

from users.models import User


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


