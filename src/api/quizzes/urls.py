from django.urls import path
from .views import QuizList, QuizDetail, ChangeAssessments
urlpatterns = [
    path('class/<int:class_pk>/tests/', QuizList.as_view(), name='test_list'),
    path('test/<int:test_pk>/', QuizDetail.as_view(), name='test_detail'),
    path('test/<int:quiz_pk>/assessments/', ChangeAssessments.as_view(), name='quiz_assessments')
]