from django.urls import path
from .views import TempQuizCreate, TempPatternList, TempPatternDetail, TempBlankList, TempBlankDetail

urlpatterns = [
    path('tests/', TempQuizCreate.as_view(), name='temp_quiz'),
    path('test/<int:test_pk>/patterns/', TempPatternList.as_view(), name='temp_patterns_list'),
    path('pattern/<int:patt_pk>/', TempPatternDetail.as_view(), name='temp_pattern_detail'),
    path('test/<int:test_pk>/blanks', TempBlankList.as_view(), name='temp_blanks'),
    path('blank/<int:blank_pk>/', TempBlankDetail.as_view(), name='temp_blank_detail'),
]
