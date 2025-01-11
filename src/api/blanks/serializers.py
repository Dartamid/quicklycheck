from rest_framework import serializers
from .models import Blank


class BlankSerializer(serializers.ModelSerializer):
    
    testName = serializers.CharField(source='test.name', read_only=True)

    class Meta:
        model = Blank
        fields = ['pk', 'quiz', 'testName', 'author', 'image', 'id_blank', 'var', 'answers']
        read_only_fields = ['image', 'author']
