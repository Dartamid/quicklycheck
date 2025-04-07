from rest_framework import serializers
from api.workshop.models import SharedQuiz


class SharedQuizSerializer(serializers.Serializer):
    class Meta:
        model = SharedQuiz
        fields = '__all__'
        