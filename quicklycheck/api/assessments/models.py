from django.db import models
from api.quizzes.models import Quiz


class Assessment(models.Model):
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='assessments')
    min_pr = models.IntegerField()
    max_pr = models.IntegerField()
    name = models.CharField(max_length=20, verbose_name='Оценка')
    color = models.CharField(max_length=6, verbose_name='Цвет отображения')
