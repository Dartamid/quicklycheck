from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from api.grades.models import Grade
from api.assessments.models import Assessment
from api.blanks.models import Blank, Score
from api.students.models import Student
from api.quizzes.models import Quiz
from api.patterns.models import Pattern, Question, AnswerChoice
from api.workshop.models import SharedQuiz

User = get_user_model()


@admin.register(Assessment)
class AssessmentsAdmin(admin.ModelAdmin):
    model = Assessment
    list_display = [field.name for field in Assessment._meta.fields]


class ScoreAdmin(admin.StackedInline):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    model = Score
    can_delete = False
    verbose_name_plural = 'Score'


class AnswerChoiceAdmin(admin.StackedInline):
    model = AnswerChoice
    can_delete = True
    verbose_name = 'Вариант ответа'
    verbose_name_plural = 'Варианты ответа'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = [field.name for field in Question._meta.fields]
    inlines = [AnswerChoiceAdmin,]
    verbose_name = 'Вопрос'
    verbose_name_plural = 'Вопросы'


@admin.register(Blank)
class BlanksAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    model = Blank
    inlines = [ScoreAdmin]
    list_display = [field.name for field in Blank._meta.fields]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    model = Grade
    list_display = ['__str__']


@admin.register(Pattern)
class PatternsAdmin(admin.ModelAdmin):
    model = Pattern
    list_display = [field.name for field in Pattern._meta.fields]


@admin.register(Quiz)
class QuizzesAdmin(admin.ModelAdmin):
    model = Quiz
    list_display = [field.name for field in Quiz._meta.fields]

@admin.register(SharedQuiz)
class SharedQuizAdmin(admin.ModelAdmin):
    model = SharedQuiz
    list_display = [field.name for field in SharedQuiz._meta.fields]

@admin.register(Student)
class StudentsAdmin(admin.ModelAdmin):
    model = Student
    list_display = [field.name for field in Student._meta.fields]
