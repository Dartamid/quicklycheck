from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.grades.models import Grade
from api.teachers.permissions import IsTeacher
from api.quizzes.models import Quiz
from api.quizzes.serializers import QuizSerializer
from api.combined.serializers import QuizDetailSerializer


class QuizList(APIView):
    model = Grade
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, class_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["class_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        tags=['Quizzes'],
        summary="Список тестов",
        description="Возвращает список тестов для пользователя",
        responses={
            200: OpenApiResponse(
                response=QuizSerializer(many=True),
                description="Список тестов",
            ),
        }
    )
    def get(self, request, class_pk):
        grade = self.get_object(class_pk)
        tests = grade.quizzes
        serialized = self.serializer_class(tests, many=True)
        return Response(serialized.data)

    @extend_schema(
        tags=['Quizzes'],
        summary="Новый тест",
        description="Создает новый тест для пользователя",
        request=QuizSerializer(),
        responses={
            201: OpenApiResponse(
                response=QuizSerializer(),
                description="Новый тест",
            ),
            400: OpenApiResponse(
                description="Ошибка валидации",
            )
        }
    )
    def post(self, request, class_pk):
        data = request.data.copy()
        data['teacher'] = request.user.pk
        data['grade'] = self.get_object(class_pk).pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetail(APIView):
    model = Quiz
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        tags=['Quizzes'],
        summary="Детализация теста",
        description="Возвращает все данные о тесте по ID",
        responses={
            200: OpenApiResponse(
                response=QuizDetailSerializer(),
                description="Тест",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному тесту",
            ),
            404: OpenApiResponse(
                description="Тест с данным ID не найден",
            )
        }
    )
    def get(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = QuizDetailSerializer(test)
        return Response(serialized.data)

    @extend_schema(
        tags=['Quizzes'],
        summary="Изменение теста",
        description="Изменяет одно или несколько полей теста по ID",
        request=QuizSerializer(),
        responses={
            200: OpenApiResponse(
                response=QuizSerializer(),
                description="Измененный тест",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному тесту",
            ),
            404: OpenApiResponse(
                description="Тест с данным ID не найден",
            )
        }
    )
    def put(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = self.serializer_class(test, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Quizzes'],
        summary="Удаление теста",
        description="Удаляет тест по ID",
        request=QuizSerializer(),
        responses={
            204: OpenApiResponse(
                description="Тест удален",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному тесту",
            ),
            404: OpenApiResponse(
                description="Тест с данным ID не найден",
            )
        }
    )
    def delete(self, request, test_pk):
        test = self.get_object(test_pk)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeAssessments(APIView):
    model = Quiz
    model = QuizDetailSerializer

    @extend_schema(
        tags=['Assessments'],
        summary="Изменение оценивания для теста",
        description="Изменяет градацию оценки для теста",
        responses={
            200: OpenApiResponse(
                description="Оценивание успешно изменено",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному тесту",
            ),
            404: OpenApiResponse(
                description="Тест с данным ID не найден",
            )
        }
    )
    def post(self, request, quiz_pk):
        try:
            assessments = request.data['assessments']
        except:
            return Response({
                "detail": 'Новое оценивание не было предоставлено',
            }, status=status.HTTP_400_BAD_REQUEST)
        quiz = get_object_or_404(Quiz, teacher=request.user, pk=quiz_pk)
        quiz.assessments = assessments
        quiz.save(update_fields=['assessments'])
        return Response(QuizDetailSerializer(quiz).data, status=status.HTTP_200_OK)
