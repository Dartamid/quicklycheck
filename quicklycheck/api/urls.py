from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ClassList, ClassDetail, PatternList,
    PatternDetail, StudentList, StudentDetail,
    BlankList, BlankDetail, UserList, TestList, TestDetail
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls')),
    path('classes/', ClassList.as_view()),
    path('class/<int:pk>/', ClassDetail.as_view()),
    path('class/<int:class_pk>/students/', StudentList.as_view()),
    path('student/<int:student_pk>/', StudentDetail.as_view()),
    path('class/<int:class_pk>/tests/', TestList.as_view()),
    path('test/<int:test_pk>/', TestDetail.as_view()),
    path('test/<int:test_pk>/patterns', PatternList.as_view()),
    path('pattern/<int:pk>', PatternDetail.as_view()),
    path('test/<int:test_pk>/blanks/', BlankList.as_view()),
    path('blank/<int:pk>/', BlankDetail.as_view()),
    path('users/', UserList.as_view())
]
