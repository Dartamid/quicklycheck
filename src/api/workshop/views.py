from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.quizzes.models import Quiz
from api.teachers.permissions import IsTeacher
from api.workshop.models import SharedQuiz
from api.workshop.serializers import SharedQuizSerializer

from copy import deepcopy


class WorkshopList(APIView):
    model = SharedQuiz
    serializer = SharedQuizSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    @extend_schema(
        tags=['Workshop'],
        summary="Список опубликованных тестов",
        description="Возвращает список опубликованных тестов",
        responses={
            200: OpenApiResponse(
                response=SharedQuizSerializer(many=True),
                description="Список опубликованных тестов"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному запросу")
        }
    )
    def get(self, request):
        shared_quizzes = SharedQuiz.objects.all()
        serialized = self.serializer(shared_quizzes, many=True)
        return Response(serialized.data)


class WorkshopQuizPublish(APIView):
    model = SharedQuiz
    serializer = SharedQuizSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    @extend_schema(
        tags=['Workshop'],
        summary="Публикация теста",
        description="Публикация нового теста в Мастерскую. Тест содержит в себе варианты, а также градацию оценивания ",
        responses={
            200: OpenApiResponse(
                response=SharedQuizSerializer(),
                description="Вариант успешно создан"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def post(self, request, quiz_pk):
        original_quiz = get_object_or_404(Quiz, pk=quiz_pk, teacher=request.user)
        clone_quiz = deepcopy(original_quiz)
        clone_quiz.id = None
        clone_quiz.save()
        shared_quiz = SharedQuiz(
            teacher=request.user,
            parent_quiz=original_quiz,
            quiz=clone_quiz,
        )
        shared_quiz.save()
        serialized = self.serializer(shared_quiz)
        return Response(serialized.data, status=status.HTTP_201_CREATED)