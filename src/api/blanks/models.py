from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.quizzes.models import Quiz
from api.students.models import Student
from django_json_field_schema_validator.validators import JSONFieldSchemaValidator


# answers_schema = {
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "type": "object",
#   "properties":{
#       str(key+1): {"type": "integer", "minimum": 0, "maximum": 12345} for key in range(40)
#   },
#   "required": [str(key+1) for key in range(40)]
# }



def json_answers():
    return [ 0 for _ in range(40)]

def json_checked_answers():
    return [ {
        'actual': 0,
        'correct': 0,
        'isRight': False,
    } for _ in range(40)]


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
    assessment = models.CharField(
        verbose_name='Оценка работы',
        null=True, blank=True,
        max_length=20
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

    def set_assessment(self):
        if self.score.is_checked:
            assessments = self.quiz.assessments
            per = self.score.percentage
            for assessment in assessments:
                if assessment['min_pr'] < per <= assessment['max_pr']:
                    self.assessment = assessment['name']


class InvalidBlank(models.Model):
    quiz = models.ForeignKey(
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


class Score(models.Model):
    blank = models.OneToOneField(Blank, on_delete=models.CASCADE, related_name='score')
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
