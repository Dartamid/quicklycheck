from django.db import models
from api.quizzes.models import Quiz, json_assessments
from api.teachers.models import User


class SharedQuiz(models.Model):
    parent_quiz = models.ForeignKey(
        Quiz, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='child_quizzes'
    )
    shared_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Shared Quiz'
        verbose_name_plural = 'Shared Quizzes'