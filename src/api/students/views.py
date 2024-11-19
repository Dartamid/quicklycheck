from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from api.students.models import Student
from api.students.serializers import StudentSerializer
from api.grades.models import Grade
from api.teachers.permissions import IsTeacher
from api.combined.serializers import StudentDetailSerializer


class StudentList(APIView):
    model = Student
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=['Students'],
        summary="Список учеников класса",
        description="Возвращает список учеников по ID класса",
        responses={
            200: OpenApiResponse(
                response=StudentSerializer(many=True),
                description="Список учеников класса",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному классу",
            ),
            404: OpenApiResponse(
                description="Класс с данным ID не найден",
            )
        }
    )
    def get(self, request, class_pk):
        user = request.user
        students = get_object_or_404(Grade, pk=class_pk, teacher=user).students
        serialized = self.serializer_class(students, many=True)
        return Response(serialized.data)

    @extend_schema(
        tags=['Students'],
        summary="Создание нового ученика",
        description="Создает нового ученика для класса с данным ID",
        request=StudentDetailSerializer(),
        responses={
            201: OpenApiResponse(
                response=StudentSerializer(),
                description="Новый ученик",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному классу",
            ),
            404: OpenApiResponse(
                description="Класс с данным ID не найден",
            )
        }
    )
    def post(self, request, class_pk):
        grade = get_object_or_404(Grade, pk=class_pk, teacher=request.user)
        data = request.data.copy()
        data['grade'] = grade.pk
        serialized = self.serializer_class(data=data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    model = Student
    serializer_class = StudentDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, student_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["student_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        tags=['Students'],
        summary="Информация о студенте",
        description="Возвращает всю информацию о студенте",
        responses={
            200: OpenApiResponse(
                response=StudentSerializer(),
                description="Информация о ученике",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному студенту",
            ),
            404: OpenApiResponse(
                description="Студент с данным ID не найден",
            )
        }
    )
    def get(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = self.serializer_class(student)
        return Response(serialized.data)

    @extend_schema(
        tags=['Students'],
        summary="Изменение данных студента",
        description="Изменяет одно или несколько полей данных о студенте",
        request=StudentDetailSerializer(),
        responses={
            200: OpenApiResponse(
                response=StudentSerializer(),
                description="Измененный студент",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному студенту",
            ),
            404: OpenApiResponse(
                description="Студент с данным ID не найден",
            )
        }
    )
    def put(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = self.serializer_class(student, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Students'],
        summary="Удаление студента",
        description="Удаляет студента и всю информацию о нем",
        responses={
            204: OpenApiResponse(
                description="Ученик удален",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному студенту",
            ),
            404: OpenApiResponse(
                description="Студент с данным ID не найден",
            )
        }
    )
    def delete(self, request, student_pk):
        student = self.get_object(student_pk)
        student.delete()
        return Response(data={'detail': 'Ученик удален!'}, status=status.HTTP_204_NO_CONTENT)
