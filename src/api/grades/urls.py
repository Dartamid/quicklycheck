from django.urls import path
from api.grades.views import GradeList, GradeDetail

urlpatterns = [
    path('classes/', GradeList.as_view(), name='class_list'),
    path('class/<int:pk>/', GradeDetail.as_view(), name='class_detail'),
]