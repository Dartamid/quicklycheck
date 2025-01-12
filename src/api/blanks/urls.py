from django.urls import path
from .views import BlankList, BlankDetail, InvalidBlankListView, InvalidBlankDetail


urlpatterns = [
    path('test/<int:quiz_pk>/blanks/', BlankList.as_view(), name='blank_list'),
    path('blank/<int:pk>/', BlankDetail.as_view(), name='blank_detail'),
    path('test/<int:quiz_pk>/invalidblanks', InvalidBlankListView.as_view(), name='invalid_blanks_list'),
    path('invalidblank/<int:blank_pk>/', InvalidBlankDetail.as_view(), name='invalid_blank_detail')
]