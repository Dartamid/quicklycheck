from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



def json_answers():
    return [ 0 for _ in range(40)]


def json_checked_answers():
    return [ {
        'actual': 0,
        'correct': 0,
        'isRight': False,
    } for _ in range(40)]


class TempQuiz(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )


class TempPattern(models.Model):
    quiz = models.ForeignKey(TempQuiz, on_delete=models.CASCADE, related_name='patterns')
    num = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pattern = models.CharField(max_length=500)

    def __str__(self):
        return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'
    
    
class TempBlank(models.Model):
    quiz = models.ForeignKey(
        TempQuiz, on_delete=models.CASCADE, related_name='blanks',
        verbose_name='Тест',
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
        default=json_answers,
        # validators=[JSONFieldSchemaValidator(schema=answers_schema)]
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    
    
class TempScore(models.Model):
    blank = models.OneToOneField(TempBlank, on_delete=models.CASCADE, related_name='score')
    is_checked = models.BooleanField(
        'Проверка проведена',
        default=False
    )
    percentage = models.FloatField(
        default=0,
        verbose_name='Процент выполнения',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    total = models.IntegerField(
        default=0,
        verbose_name='Процент выполнения',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(40)
        ]
    )
    right = models.IntegerField(
        default=0,
        verbose_name='Процент выполнения',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(40)
        ]
    )
    checked_answers = models.JSONField(
        default=json_checked_answers
    )