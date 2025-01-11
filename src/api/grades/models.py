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
        return f'{self.number}{self.letter} {self.teacher}'

    def get_stats(self):
        serializer = GradeStatsSerializer()
        quizzes = self.quizzes.all()
        
        serializer.studentsCount = self.students.all().count()
        serializer.blanksCount = sum([quiz.blanks_count() for quiz in quizzes])
        serializer.quizzesCount = quizzes.count()
        serializer.invalidBlanksCount = sum([quiz.invalid_blanks_count() for quiz in quizzes])


        blanks = []
        for quiz in list(quizzes):
            quiz_blanks = list(quiz.blanks.all())
            blanks += [*quiz_blanks]
        
        serializer.fullworks = len(list(filter(lambda x: x.score.percentage == 100, blanks)))

        if serializer.studentsCount > 0:
            students = [(student, student.get_avg()) for student in self.students.all()]
            students_by_avg = sorted(students, key=lambda x: x[1], reverse=True)

            serializer.bestAvg = students_by_avg[0][1]
            serializer.worstAvg = students_by_avg[-1][1]
            serializer.avgScore = sum([blank.score.percentage for blank in blanks]) / len(blanks)

        return serializer