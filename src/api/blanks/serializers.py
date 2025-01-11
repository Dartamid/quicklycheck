from rest_framework import serializers
from .models import Blank, Score


class ScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Score
        fields = '__all__'


class BlankSerializer(serializers.ModelSerializer):
    score = ScoreSerializer(source='score', read_only=True)
    testName = serializers.CharField(source='test.name', read_only=True)
    

    class Meta:
        model = Blank
        fields = ['pk', 'quiz', 'testName', 'author', 'image', 'id_blank', 'var', 'answers', 'score']
        read_only_fields = ['image', 'author']

