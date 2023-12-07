from django.urls import path, include
from .views import (
    ClassList, ClassDetail, PatternList,
    PatternDetail, StudentList, StudentDetail,
    BlankList, BlankDetail
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('classes/', ClassList.as_view()),
    path('class/<int:pk>/', ClassDetail.as_view()),
    path('class/<int:class_pk>/students/', StudentList.as_view()),
    path('student/<int:pk>/', StudentDetail.as_view()),
    path('test/<int:test_pk>/patterns', PatternList.as_view()),
    path('pattern/<int:pk>', PatternDetail.as_view()),
    path('test/<int:test_pk>/blanks/', BlankList.as_view()),
    path('blank/<int:pk>/', BlankDetail.as_view()),
]