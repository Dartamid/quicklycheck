from django.urls import path
from .views import index, list_classes, add_class, class_detail, add_student, add_test, test_detail, add_pattern, \
    add_blanks, blank_detail, delete_class, download

urlpatterns = [
    path('', index, name='index'),
    path('download/', download, name='download'),
    path('myclasses/', list_classes, name='myclasses'),
    path('add_class/', add_class, name='add_class'),
    path('class_detail/<int:class_pk>', class_detail, name='class_detail'),
    path('test_detail/<int:test_pk>', test_detail, name='test_detail'),
    path('add_student/<int:class_pk>', add_student, name='add_student'),
    path('add_test/<int:class_pk>', add_test, name='add_test'),
    path('add_pattern/<int:test_pk>', add_pattern, name='add_pattern'),
    path('add_blanks/<int:test_pk>', add_blanks, name='add_blanks'),
    path('blank_detail/<int:blank_pk>', blank_detail, name='blank_detail'),
    path('delete_class/<int:class_pk>', delete_class, name='delete_class')
]
