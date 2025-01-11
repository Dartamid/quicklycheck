from rest_framework import serializers
from .models import Blank, Score, InvalidBlank


class ScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Score
        fields = ('is_checked', 'percentage', 'total', 'right', 'checked_answers')


class BlankSerializer(serializers.ModelSerializer):
    blank_score = ScoreSerializer(source='score', read_only=True)
    testName = serializers.CharField(source='quiz.name', read_only=True)
    

    class Meta:
        model = Blank
        fields = ['pk', 'quiz', 'testName', 'author', 'image', 'id_blank', 'var', 'answers', 'blank_score', 'created_at']
        read_only_fields = ['image', 'author']


class InvalidBlankSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InvalidBlank
        fields = ['quiz', 'image', 'created_at']
        read_only_fields = ['image']