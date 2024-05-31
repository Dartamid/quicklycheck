from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ClassList, ClassDetail, PatternList,
    PatternDetail, StudentList, StudentDetail,
    BlankList, BlankDetail, UserList, TestList, TestDetail, TempTestList, TempPatternList, TempBlankList,
    TempPatternDetail, TempBlankDetail, ChangePasswordView, AssessmentList, AssessmentDetail, CreateUserView
)

urls_auth = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/', include('rest_framework.urls')),
]

urls_temp = [
    path('temp/tests/', TempTestList.as_view(), name='temp_list'),
    path('temp/test/<int:test_pk>/patterns/', TempPatternList.as_view(), name='temp_pattern_list'),
    path('temp/pattern/<int:patt_pk>/', TempPatternDetail.as_view(), name='temp_pattern_detail'),
    path('temp/test/<int:test_pk>/blanks/', TempBlankList.as_view(), name='temp_blank_list'),
    path('temp/blank/<int:pk>/', TempBlankDetail.as_view(), name='temp_blank_detail')
]

urls_class = [
    path('classes/', ClassList.as_view(), name='class_list'),
    path('class/<int:pk>/', ClassDetail.as_view(), name='class_detail'),
]

urls_students = [
    path('class/<int:class_pk>/students/', StudentList.as_view(), name='student_list'),
    path('student/<int:student_pk>/', StudentDetail.as_view(), name='student_detail'),
]

urls_test = [
    path('class/<int:class_pk>/tests/', TestList.as_view(), name='test_list'),
    path('test/<int:test_pk>/', TestDetail.as_view(), name='test_detail'),
]

# Обернуто
urls_users = [
    path('users/', UserList.as_view(), name='user_list'),
    path('registration/', CreateUserView.as_view(), name='register'),
    path('user/password_change/', ChangePasswordView.as_view(), name='password_change'),
]

urls_patterns = [
    path('test/<int:test_pk>/patterns/', PatternList.as_view(), name='pattern_list'),
    path('pattern/<int:patt_pk>', PatternDetail.as_view(), name='pattern_detail'),
]

urls_assessment = [
    path('test/<int:test_pk>/assessment/', AssessmentList.as_view(), name='assessment_list'),
    path('assessment/<int:pk>/', AssessmentDetail.as_view(), name='assessment_detail'),
]

urls_blanks = [
    path('test/<int:test_pk>/blanks/', BlankList.as_view(), name='blank_list'),
    path('blank/<int:pk>/', BlankDetail.as_view(), name='blank_detail'),
]


urls_list = [
    urls_auth, urls_users, urls_temp,
    urls_test, urls_patterns, urls_assessment,
    urls_class, urls_blanks, urls_students,
]
urlpatterns = []

for inner_urls in urls_list:
    urlpatterns.extend(inner_urls)
