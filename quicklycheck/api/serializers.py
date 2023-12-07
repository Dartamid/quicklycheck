from rest_framework import serializers
from checker.models import Class, Student, Test, Pattern, Blank


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['number', 'letter', 'created_date']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'teacher']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['teacher', 'grade', 'teacher']


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['test', 'num', 'pattern']


class BlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = ['pk', 'test', 'author', 'id_blank', 'var', 'answers']

