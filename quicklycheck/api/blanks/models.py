from django.db import models
from api.quizzes.models import Quiz
from api.students.models import Student


class Blank(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='blanks')
    author = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='works', blank=True, null=True)
    id_blank = models.CharField(max_length=2)
    var = models.IntegerField()
    image = models.ImageField(
        'Фотография бланка',
        upload_to='blanks/',
    )
    answers = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)


class InvalidBlank(models.Model):
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='invalid_blanks')
    image = models.ImageField(
        'Фотография бланка',
        upload_to='invalid_blanks/',
    )
    created_at = models.DateTimeField(auto_now_add=True)
