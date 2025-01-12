from rest_framework import serializers
from .models import Blank, Score, InvalidBlank
from api.students.serializers import StudentSerializer
from api.grades.serializers import GradeSerializer


class ScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Score
        fields = ('is_checked', 'percentage', 'total', 'right', 'checked_answers')


class BlankSerializer(serializers.ModelSerializer):
    blank_score = ScoreSerializer(source='score', read_only=True)
    testName = serializers.CharField(source='quiz.name', read_only=True)
    author_info = StudentSerializer(source='author', read_only=True)
    

    class Meta:
        model = Blank
        fields = ['pk', 'quiz', 'testName', 'author_info', 'image', 'id_blank', 'var', 'answers', 'blank_score', 'created_at']
        read_only_fields = ['image', 'author_info']


class InvalidBlankSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True, source='quiz.grade')

    class Meta:
        model = InvalidBlank
        fields = ['pk', 'quiz', 'image', 'grade' ,'created_at']
        read_only_fields = ['image']