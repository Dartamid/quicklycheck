from rest_framework import serializers

from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['pk', 'name']