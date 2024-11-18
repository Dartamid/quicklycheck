from django.urls import path
from .views import AssessmentList, AssessmentDetail


urlpatterns = [
    path('test/<int:test_pk>/assessment/', AssessmentList.as_view(), name='assessment_list'),
    path('assessment/<int:pk>/', AssessmentDetail.as_view(), name='assessment_detail'),
]
