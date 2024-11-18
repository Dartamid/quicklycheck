from rest_framework import serializers

#
# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Test
#         fields = ['pk', 'name']
#
#
# class TempTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempTest
#         fields = ['pk']
#
#
# class TempPatternSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempPattern
#         fields = ['pk', 'test', 'num', 'pattern']
#
#
# class TempBlankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempBlank
#         fields = ['pk', 'test', 'image', 'id_blank', 'var', 'answers']