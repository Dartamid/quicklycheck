from django.contrib.auth import get_user_model
from django.db import models
from api.stats.serializers import StudentStatsSerializer
from api.grades.models import Grade

User = get_user_model()


class Student(models.Model):
    name = models.CharField(max_length=254)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f'{self.name} {self.grade}'
    
    def get_avg(self):
        blanks = self.works.all()
        if len(blanks) > 0:
            avg = sum([blank.score.percentage for blank in blanks]) / len(blanks)
            return avg
        return 0
    
    def get_stats(self):
        serializer = StudentStatsSerializer()
        blanks = self.works.all().order_by("score__percentage")

        if len(blanks) > 0:
            serializer.worstWork = blanks.first().score.percentage
            serializer.bestWork = blanks.last().score.percentage

        return serializer


    class Meta:
        ordering = ('name',)
