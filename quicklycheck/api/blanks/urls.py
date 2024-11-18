from django.urls import path
from .views import BlankList, BlankDetail


urlpatterns = [
    path('test/<int:test_pk>/blanks/', BlankList.as_view(), name='blank_list'),
    path('blank/<int:pk>/', BlankDetail.as_view(), name='blank_detail'),
]