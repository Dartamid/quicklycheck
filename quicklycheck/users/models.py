from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
