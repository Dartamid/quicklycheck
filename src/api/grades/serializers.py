from rest_framework import serializers
from api.stats.serializers import GradeStatsSerializer
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['pk', 'number', 'letter',]
