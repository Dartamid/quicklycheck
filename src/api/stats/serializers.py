from rest_framework import serializers


class GradeStatsSerializer(serializers.Serializer):
    studentsCount = serializers.IntegerField()
    quizzesCount = serializers.IntegerField()
    blanksCount = serializers.IntegerField()
    invalidBlanksCount = serializers.IntegerField()
    avgScore = serializers.FloatField()
    
    class Meta:
        fields = ['--all--']