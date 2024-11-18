from django.urls import path
from .views import PatternList, PatternDetail

urlpatterns = [
    path('test/<int:test_pk>/patterns/', PatternList.as_view(), name='pattern_list'),
    path('pattern/<int:patt_pk>/', PatternDetail.as_view(), name='pattern_detail'),
]
