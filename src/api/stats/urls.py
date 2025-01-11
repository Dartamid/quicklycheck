from django.urls import path
from api.stats.views import GradeStatsByPeriodView

urlpatterns = [
    path('stats/class/<int:grade_pk>/<str:period>/', GradeStatsByPeriodView.as_view(), name='grade_graph'),
]