from rest_framework import serializers
from .models import TempQuiz, TempPattern, TempBlank


class TempQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempQuiz
        fields = ['pk']


class TempPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPattern
        fields = ['pk', 'quiz', 'num', 'pattern']


class TempBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempBlank
        fields = ['pk', 'quiz', 'image', 'id_blank', 'var', 'answers']