from django.contrib.auth import get_user_model
from django.db import models

from ..grades.models import Grade

User = get_user_model()


class Student(models.Model):
    name = models.CharField(max_length=254)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f'{self.name} {self.grade}'

    class Meta:
        ordering = ('name',)
