from django.urls import path
from api.stats.views import GradeStatsByPeriodView

urlpatterns = [
    path('stats/class/<int:grade_pk>/', GradeStatsByPeriodView.as_view(), name=''),
]