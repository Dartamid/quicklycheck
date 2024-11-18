from rest_framework import serializers
from api.teachers.serializers import TeacherSerializer
from api.blanks.serializers import BlankSerializer
from api.quizzes.serializers import QuizSerializer
from api.students.serializers import StudentSerializer
from api.grades.serializers import GradeSerializer
from api.grades.models import Grade
from api.students.models import Student


class StudentDetailSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    works = BlankSerializer(many=True, read_only=True, source='works.all')
    grade_detail = GradeSerializer(read_only=True, source='grade')

    class Meta:
        model = Student
        fields = ['pk', 'name', 'grade_detail', 'teacher_detail', 'works']


class GradeDetailSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    quizzes = QuizSerializer(source='quizzes.all', many=True, read_only=True)
    students = StudentSerializer(source='students.all', many=True, read_only=True)

    class Meta:
        model = Grade
        fields = ['pk', 'number', 'letter', 'teacher_detail', 'quizzes', 'students']
