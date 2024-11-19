from django.db import models
from django.contrib.auth import get_user_model
from api.grades.models import Grade


User = get_user_model()


class Quiz(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=254)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='quizzes')

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name
