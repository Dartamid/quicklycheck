from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.quizzes.models import Quiz


class Assessment(models.Model):
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='assessments')
    min_pr = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
    ])
    max_pr = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
    ])
    name = models.CharField(max_length=20, verbose_name='Оценка')
    color = models.CharField(max_length=6, verbose_name='Цвет отображения')
