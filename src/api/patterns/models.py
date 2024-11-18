from django.db import models
from api.quizzes.models import Quiz


class Pattern(models.Model):
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='patterns')
    num = models.IntegerField()
    pattern = models.CharField(max_length=500)

    def __str__(self):
        return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'
