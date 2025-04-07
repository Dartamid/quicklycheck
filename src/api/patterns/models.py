from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from api.quizzes.models import Quiz
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


types_questions = [
    ('OP', 'Open'),
    ('CL', 'Close')
]

answers_type = [
    (1, 'Первый'),
    (2, 'Второй'),
    (3, 'Третий'),
    (4, 'Четвертый'),
    (5, 'Пятый'),
    (6, 'Открытый')
]


class Pattern(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='patterns')
    num = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pattern = models.CharField(max_length=500)
    extended = models.BooleanField('Расширенный', default=False)


    def __str__(self):
        return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'


class Question(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Тело вопроса', blank=True, null=True)
    question_type = models.CharField(max_length=2, choices=types_questions)
    position = models.IntegerField(
        verbose_name='Номер вопроса',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )


class AnswerChoice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answer_choices',
        blank=True, null=True
    )
    choice = models.CharField(choices=answers_type, max_length=1)
    answer_text = models.CharField('Вариант ответа', max_length=200, blank=True, null=True)
    is_right = models.BooleanField('Правильный', default=False)