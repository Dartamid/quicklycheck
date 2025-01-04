from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from api.quizzes.models import Quiz

User = get_user_model()


class Pattern(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='patterns')
    num = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pattern = models.CharField(max_length=500)

    def __str__(self):
        return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'
