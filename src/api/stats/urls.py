from django.urls import path
from api.stats.views import GradeStatsByPeriodView, QuizGraphsView

urlpatterns = [
    path('stats/class/<int:grade_pk>/', GradeStatsByPeriodView.as_view(), name='grade_graph'),
    path('stats/quiz/<int:quiz_pk>/', QuizGraphsView.as_view(), name='quiz_graph'),
    path('stats/student/<int:students_pk>/', GradeStatsByPeriodView.as_view(), name='students_graph'),
]