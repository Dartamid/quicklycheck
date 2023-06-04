from django.contrib import admin
from .models import Class, Test, Blank, Pattern, Student


# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    pass


@admin.register(Blank)
class BlankAdmin(admin.ModelAdmin):
    pass

