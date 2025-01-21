from rest_framework import serializers
from .models import TempQuiz, TempPattern, TempBlank, TempScore


class TempScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TempScore
        fields = ('is_checked', 'percentage', 'total', 'right', 'checked_answers')


class TempQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempQuiz
        fields = ['pk']


class TempPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPattern
        fields = ['pk', 'quiz', 'num', 'pattern']


class TempBlankSerializer(serializers.ModelSerializer):
    blank_score = TempScoreSerializer(source='score', read_only=True)

    class Meta:
        model = TempBlank
        fields = ['pk', 'quiz', 'image', 'assessments', 'id_blank', 'var', 'answers', 'blank_score']