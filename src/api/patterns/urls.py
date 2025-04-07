from django.urls import path
from .views import PatternList, PatternDetail, QuestionList, QuestionDetail, AnswerChoiceList, AnswerChoicesDetail

urlpatterns = [
    path('test/<int:test_pk>/patterns/', PatternList.as_view(), name='pattern_list'),
    path('pattern/<int:patt_pk>/', PatternDetail.as_view(), name='pattern_detail'),
    path('pattern/<int:patt_pk>/questions/', QuestionList.as_view(), name='questions_list'),
    path('questions/<int:question_pk>/', QuestionDetail.as_view(), name='question_detail'),
    path('question/<int:question_pk>/answers/', AnswerChoiceList.as_view(), name='answer_choices_list'),
    path('answers/<int:answer_pk>/', AnswerChoicesDetail.as_view(), name='answer_choice_detail')
]
