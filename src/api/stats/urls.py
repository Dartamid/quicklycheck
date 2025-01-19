from django.urls import path
from api.stats.views import GradeStatsByPeriodView, QuizGraphsView, StudentGraphsView

urlpatterns = [
    path('stats/class/<int:grade_pk>/', GradeStatsByPeriodView.as_view(), name='grade_graph'),
    path('stats/quiz/<int:quiz_pk>/', QuizGraphsView.as_view(), name='quiz_graph'),
    path('stats/student/<int:student_pk>/', StudentGraphsView.as_view(), name='students_graph'),
]