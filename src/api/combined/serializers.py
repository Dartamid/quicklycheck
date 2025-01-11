from rest_framework import serializers
from api.teachers.serializers import TeacherSerializer
from api.blanks.serializers import BlankSerializer, InvalidBlankSerializer
from api.quizzes.serializers import QuizShortSerializer
from api.students.serializers import StudentShortSerializer
from api.grades.serializers import GradeSerializer
from api.stats.serializers import GradeStatsSerializer
from api.grades.models import Grade
from api.students.models import Student
from api.quizzes.models import Quiz
from api.stats.serializers import StudentStatsSerializer



class StudentDetailSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher.account', read_only=True)
    works = BlankSerializer(many=True, read_only=True, source='works.all')
    grade_detail = GradeSerializer(read_only=True, source='grade')
    stats = StudentStatsSerializer(read_only=True, source='get_stats')

    class Meta:
        model = Student
        fields = ['pk', 'name', 'stats' , 'grade_detail', 'teacher_detail', 'works']


class GradeDetailSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(
        source='teacher.account', read_only=True
    )
    quizzes = QuizShortSerializer(
        source='quizzes.all', many=True, read_only=True
    )
    students = StudentShortSerializer(
        source='students.all', many=True, read_only=True,
    )
    stats = GradeStatsSerializer(
        source='get_stats', read_only=True
    )

    class Meta:
        model = Grade
        fields = ['pk', 'number', 'letter', 'stats', 'teacher_detail', 'quizzes', 'students']


class QuizDetailSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    blanks = BlankSerializer(many=True, read_only=True, source='valid_blanks')
    without_pattern = BlankSerializer(many=True, read_only=True, source='without_pattern_blanks')
    invalid_blanks = InvalidBlankSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['pk', 'name', 'grade', 'blanks', 'without_pattern', 'invalid_blanks']