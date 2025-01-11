from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from api.grades.models import Grade
from api.assessments.models import Assessment
from api.blanks.models import Blank, Score
from api.students.models import Student
from api.patterns.models import Pattern
from api.quizzes.models import Quiz

User = get_user_model()


@admin.register(Assessment)
class AssessmentsAdmin(admin.ModelAdmin):
    model = Assessment
    list_display = [field.name for field in Assessment._meta.fields]


class ScoreAdmin(admin.StackedInline):
    model = Score
    can_delete = False
    verbose_name_plural = 'Score'
    

@admin.register(Blank)
class BlanksAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    model = Blank
    list_display = [field.name for field in Blank._meta.fields] + [ScoreAdmin]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    model = Grade
    list_display = [field.name for field in Grade._meta.fields]


@admin.register(Pattern)
class PatternsAdmin(admin.ModelAdmin):
    model = Pattern
    list_display = [field.name for field in Pattern._meta.fields]


@admin.register(Quiz)
class QuizzesAdmin(admin.ModelAdmin):
    model = Quiz
    list_display = [field.name for field in Quiz._meta.fields]


@admin.register(Student)
class StudentsAdmin(admin.ModelAdmin):
    model = Student
    list_display = [field.name for field in Student._meta.fields]
