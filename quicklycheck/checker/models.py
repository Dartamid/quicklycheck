from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Class(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')
    number = models.CharField(max_length=2)
    letter = models.CharField(max_length=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number + self.letter


class Student(models.Model):
    name = models.CharField(max_length=254)
    grade = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='students')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f'{self.name} {self.grade}'

    class Meta:
        ordering = ('name',)


class Test(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(max_length=254)
    grade = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        return self.name


class Pattern(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='patterns')
    num = models.IntegerField()
    pattern = models.CharField(max_length=500)

    def __str__(self):
        return f'Вариант {self.num} - {len(self.pattern.split(","))}/40'


class Blank(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='blanks')
    author = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='works')
    id_blank = models.CharField(max_length=2)
    var = models.IntegerField()
    image = models.ImageField(
        'Фотография бланка',
        upload_to='blanks/',
    )
    answers = models.CharField(max_length=254)
