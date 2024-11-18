from rest_framework import serializers
from .models import Assessment


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['pk', 'name', 'color', 'min_pr', 'max_pr']
