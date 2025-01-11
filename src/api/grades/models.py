from django.db import models
from django.contrib.auth import get_user_model
from api.stats.serializers import GradeStatsSerializer

User = get_user_model()


class Grade(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    number = models.CharField(max_length=2)
    letter = models.CharField(max_length=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number + self.letter

    def get_stats(self):
        serializer = GradeStatsSerializer()
        quizzes = self.quizzes.all()
        
        serializer.studentsCount = self.students.all().count()
        serializer.blanksCount = sum([quiz.blanks_count() for quiz in quizzes])
        serializer.quizzesCount = quizzes.count()
        serializer.invalidBlanksCount = sum([quiz.invalid_blanks_count() for quiz in quizzes])
        serializer.avgScore = avg([blank for test in list(quiz.blanks.all()) for quiz in quizzes], key= lambda x: x.score.percentage)
        
        return serializer