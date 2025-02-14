from rest_framework import serializers
from .models import Pattern


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['pk', 'quiz', 'num', 'pattern', 'teacher']
