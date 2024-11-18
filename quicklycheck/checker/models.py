from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

#
# class TempQuiz(models.Model):
#     name = models.CharField(max_length=254, blank=None, null=True)
#
#
# class TempPattern(models.Model):
#     test = models.ForeignKey('TempTest', on_delete=models.CASCADE, related_name='patterns')
#     num = models.IntegerField()
#     pattern = models.CharField(max_length=500)
#
#     def __str__(self):
#         return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'
#
#
# class TempBlank(models.Model):
#     test = models.ForeignKey('TempTest', on_delete=models.CASCADE, related_name='blanks')
#     id_blank = models.CharField(max_length=2, blank=True, null=True)
#     var = models.IntegerField()
#     image = models.ImageField(
#         'Фотография бланка',
#         upload_to='blanks/',
#     )
#     answers = models.CharField(max_length=254)
