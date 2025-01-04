from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.quizzes.models import Quiz
from api.students.models import Student


class Blank(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='blanks',
        verbose_name='Тест',
    )
    author = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='works', 
        blank=True, null=True, verbose_name='Ученик',
    )
    id_blank = models.CharField(
        max_length=2, verbose_name='ID ученика'
    )
    var = models.IntegerField(
        verbose_name='Вариант',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    image = models.ImageField(
        'Фотография бланка',
        upload_to='blanks/',
    )
    answers = models.JSONField(
        verbose_name='Ответы',
        default={str(key+1): 0 for key in range(40)}
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )


class InvalidBlank(models.Model):
    test = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='invalid_blanks',
        verbose_name='Тест'
    )
    image = models.ImageField(
        'Фотография бланка',
        upload_to='invalid_blanks/',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
