from django.db import models
from django.contrib.auth import get_user_model

from ..blanks.models import Blank

User = get_user_model()


class Feedback(models.Model):
    text = models.TextField(
        verbose_name="Текст",
        max_length=1000,
    )
    blank = models.ForeignKey(Blank, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    type_error = models.IntegerField(default=0)

