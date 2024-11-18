from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urls_auth = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urls_temp = [
#     path('temp/tests/', TempTestList.as_view(), name='temp_list'),
#     path('temp/test/<int:test_pk>/patterns/', TempPatternList.as_view(), name='temp_pattern_list'),
#     path('temp/pattern/<int:patt_pk>/', TempPatternDetail.as_view(), name='temp_pattern_detail'),
#     path('temp/test/<int:test_pk>/blanks/', TempBlankList.as_view(), name='temp_blank_list'),
#     path('temp/blank/<int:pk>/', TempBlankDetail.as_view(), name='temp_blank_detail')
# ]


urlpatterns = [
    path('assessments/', include('api.assessments.urls')),
    path('students/', include('api.students.urls')),
    path('teachers/', include('api.teachers.urls')),
    path('blanks/', include('api.blanks.urls')),
    path('grades/', include('api.grades.urls')),
    # path('feedbacks/', include('api.feedbacks.urls')),
    path('quizzes/', include('api.quizzes.urls')),
    path('temps/', include('api.temps.urls')),
]

urlpatterns.extend(urls_auth)
