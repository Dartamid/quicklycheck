from django.urls import path, include

# urls_temp = [
#     path('temp/tests/', TempTestList.as_view(), name='temp_list'),
#     path('temp/test/<int:test_pk>/patterns/', TempPatternList.as_view(), name='temp_pattern_list'),
#     path('temp/pattern/<int:patt_pk>/', TempPatternDetail.as_view(), name='temp_pattern_detail'),
#     path('temp/test/<int:test_pk>/blanks/', TempBlankList.as_view(), name='temp_blank_list'),
#     path('temp/blank/<int:pk>/', TempBlankDetail.as_view(), name='temp_blank_detail')
# ]


urlpatterns = [
    path('', include('api.assessments.urls')),
    path('', include('api.students.urls')),
    path('', include('api.teachers.urls')),
    path('', include('api.blanks.urls')),
    path('', include('api.patterns.urls')),
    path('', include('api.grades.urls')),
    path('', include('api.quizzes.urls')),
    path('', include('api.stats.urls')),
    path('', include('api.temps.urls')),
    path('', include('api.tokens.urls')),
]


