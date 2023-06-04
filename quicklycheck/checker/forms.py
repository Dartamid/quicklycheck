from django import forms
from .models import Class, Student, Test, Pattern


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('number', 'letter',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name',)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', )


class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ('num', 'pattern',)

