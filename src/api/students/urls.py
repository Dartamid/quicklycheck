from django.urls import path
from .views import StudentList, StudentDetail

urlpatterns = [
    path('class/<int:class_pk>/students/', StudentList.as_view(), name='student_list'),
    path('student/<int:student_pk>/', StudentDetail.as_view(), name='student_detail'),
]
