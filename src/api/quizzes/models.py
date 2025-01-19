from django.db import models
from django.contrib.auth import get_user_model
from api.grades.models import Grade
from api.stats.serializers import QuizStatsSerializer


User = get_user_model()

def json_assessments():
    default = [
        {
            'name': '2',
            'minPr': 0,
            'maxPr': 40,
            'color': '#ff0000',
        },
        {
            'name': '3',
            'minPr': 40,
            'maxPr': 60,
            'color': '#ff0000',
        },
        {
            'name': '4',
            'minPr': 60,
            'maxPr': 80,
            'color': '#ff0000',
        },
        {
            'name': '5',
            'minPr': 80,
            'maxPr': 100,
            'color': '#ff0000',
        }
    ]
    return default


class Quiz(models.Model):
    assessments = models.JSONField(
        'Градация оценок',
        default=json_assessments
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=254)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='quizzes')

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name
    
    def blanks_count(self):
        return self.blanks.all().count()
    
    def invalid_blanks_count(self):
        return self.invalid_blanks.all().count()
    
    def valid_blanks(self):
        return self.blanks.filter(score__is_checked=True)
    
    def without_pattern_blanks(self):
        return self.blanks.filter(score__is_checked=False)
    
    def get_stats(self):
        serializer = QuizStatsSerializer()
        blanks = self.blanks.all().order_by('score__percentage')

        if len(blanks) > 0:
            serializer.worstWork = blanks.first().score.percentage
            scores = []
            for blank in blanks:
                scores.append(blank.score.percentage)
            serializer.avgScore = sum(scores) / len(blanks)

        return serializer

        