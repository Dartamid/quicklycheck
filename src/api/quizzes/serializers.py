from rest_framework import serializers

from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['pk', 'assessments', 'name', 'teacher', 'grade']


class QuizShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['pk', 'name']