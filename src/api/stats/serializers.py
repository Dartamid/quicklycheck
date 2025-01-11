from rest_framework import serializers


class GradeStatsSerializer(serializers.Serializer):
    studentsCount = serializers.IntegerField(default=0)
    quizzesCount = serializers.IntegerField(default=0)
    blanksCount = serializers.IntegerField(default=0)
    invalidBlanksCount = serializers.IntegerField(default=0)
    avgScore = serializers.FloatField(default=0)
    bestAvg = serializers.FloatField(default=0)
    worstAvg = serializers.FloatField(default=0)
    fullWorks = serializers.IntegerField(default=0)
    
    class Meta:
        fields = ['--all--']


class QuizStatsSerializer(serializers.Serializer):
    blanksCount = serializers.IntegerField(default=0)
    invalidBlanksCount = serializers.IntegerField(default=0)
    avgScore = serializers.FloatField(default=0)
    bestWork = serializers.FloatField(default=0)
    worstWork = serializers.FloatField(default=0)
    fullWorks = serializers.IntegerField(default=0)
    
    class Meta:
        fields = ['--all--']