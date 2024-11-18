from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Grade(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    number = models.CharField(max_length=2)
    letter = models.CharField(max_length=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number + self.letter
