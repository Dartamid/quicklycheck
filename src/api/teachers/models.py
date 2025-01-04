from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return self.account.__str__()
        


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True, default='')
    last_name = models.CharField(max_length=100, blank=True, null=True, default='')
    patronymic = models.CharField(max_length=100, blank=True, null=True, default='')
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'
