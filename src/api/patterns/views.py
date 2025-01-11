from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .serializers import PatternSerializer
from api.teachers.permissions import IsTeacher
from api.patterns.models import Pattern
from api.quizzes.models import Quiz


class PatternList(APIView):
    model = Pattern
    serializer = PatternSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    @extend_schema(
        tags=['Patterns'],
        summary="Список вариантов",
        description="Возвращает список вариантов для Теста с ID <pk>",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=PatternSerializer(many=True),
                description="Список вариантов"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def get(self, request, test_pk):
        user = request.user
        patterns = get_object_or_404(Quiz, pk=test_pk, teacher=user).patterns
        serialized = self.serializer(patterns, many=True)
        return Response(serialized.data)

    @extend_schema(
        tags=['Patterns'],
        summary="Создание нового варианта",
        description="Создает новый вариант для Теста с ID <pk>. Вариант содержит в себе свой номер, а также варианты "
                    "ответов на вопросы в тесте.",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=PatternSerializer(),
                description="Вариант успешно создан"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def post(self, request, test_pk):
        test = get_object_or_404(Quiz, pk=test_pk, teacher=request.user)
        data = request.data.copy()
        data['quiz'] = test.pk
        data['teacher'] = test.teacher.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class PatternDetail(APIView):
    model = Pattern
    serializer = PatternSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, patt_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["patt_pk"])
        self.check_object_permissions(self.request, obj.test)
        return obj

    @extend_schema(
        tags=['Patterns'],
        summary="Детализация варианта",
        description="Получение варианта по ID <pk>",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=PatternSerializer(),
                description="Вариант"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту"),
            404: OpenApiResponse(description="Вариант с данным ID не найден")
        }
    )
    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern)
        return Response(serialized.data)

    @extend_schema(
        tags=['Patterns'],
        summary="Изменение варианта",
        description="Изменяет одно или несколько полей в модели Варианта с ID <pk>.",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=PatternSerializer(),
                description="Вариант"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту"),
            404: OpenApiResponse(description="Вариант с данным ID не найден")
        }
    )
    def put(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Patterns'],
        summary="Удаление варианта",
        description="Удаление варианта с ID <pk>.",
        request=PatternSerializer,
        responses={
            204: OpenApiResponse(
                description="Вариант удален"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту"),
            404: OpenApiResponse(description="Вариант с данным ID не найден")
        }
    )
    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)