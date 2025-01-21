from rest_framework.views import APIView
from .models import TempQuiz, TempBlank, TempPattern, TempScore
from .serializers import TempQuizSerializer, TempBlankSerializer, TempPatternSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from checker.utils import checker
from PIL import Image
from io import BytesIO
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.blanks.views import check_blank


class TempQuizCreate(APIView):
    model = TempQuiz
    serializer = TempQuizSerializer

    @extend_schema(
        tags=['Temps'],
        summary="Создание временного теста",
        description="Создание временного теста для незарегистрированного пользователя",
        responses={
            201: OpenApiResponse(
                response=TempQuizSerializer(many=False),
                description="Временный вариант создан"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному запросу"),
        }
    )
    def post(self, request):
        test = self.model.objects.create()
        serialized = self.serializer(test)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class TempPatternList(APIView):
    model = TempPattern
    serializer = TempPatternSerializer

    @extend_schema(
        tags=['Temps'],
        summary="Получение списка вариантов временного теста",
        description="Получение правильных вариантов ответа для временного теста с pk=test_pk",
        responses={
            200: OpenApiResponse(
                response=TempPatternSerializer(many=True),
                description="Список варинатов временного теста"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Временный тест с данным ID не найден")
        }
    )
    def get(self, request, test_pk):
        test = get_object_or_404(TempQuiz, pk=test_pk)
        patterns = self.model.objects.filter(quiz=test)
        serialized = self.serializer(patterns, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Temps'],
        summary="Создание варианта временного теста",
        description="Создание нового варианта ответа для временного теста с pk=test_pk",
        request=TempPatternSerializer,
        responses={
            201: OpenApiResponse(
                response=TempPatternSerializer(many=False),
                description="Новый вариант временного теста"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            400: OpenApiResponse(description="Ошибка заполнения данных"),
            404: OpenApiResponse(description="Временный тест с данным ID не найден")
        }
    )
    def post(self, request, test_pk):
        test = get_object_or_404(TempQuiz, pk=test_pk)
        data = request.data.copy()
        data['test'] = test.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class TempPatternDetail(APIView):
    model = TempPattern
    serializer = TempPatternSerializer

    @extend_schema(
        tags=['Temps'],
        summary="Получение детализации варианта временного теста",
        description="Получение детализации варианта ответа для временного теста с pk=patt_pk",
        request=TempPatternSerializer,
        responses={
            200: OpenApiResponse(
                response=TempPatternSerializer(many=False),
                description="Вариант временного теста"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Вариант ответов с данным ID не найден")
        }
    )
    def get(self, request, patt_pk):
        pattern = get_object_or_404(self.model, pk=patt_pk)
        serialized = self.serializer(pattern)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Temps'],
        summary="Изменение варианта временного теста",
        description="Изменение варианта ответа для временного теста с pk=patt_pk",
        request=TempPatternSerializer,
        responses={
            200: OpenApiResponse(
                response=TempPatternSerializer(many=False),
                description="Изменения в вариант временного теста применены"
            ),
            400: OpenApiResponse(description="Ошибка ввода данных"),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту ответов"),
            404: OpenApiResponse(description="Временный тест с данным ID не найден")
        }
    )
    def put(self, request, patt_pk):
        pattern = get_object_or_404(self.model, pk=patt_pk)
        serialized = self.serializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Temps'],
        summary="Удаление варианта временного теста",
        description="Удаление варианта ответа для временного теста с pk=patt_pk",
        responses={
            204: OpenApiResponse(
                response=TempPatternSerializer(many=False),
                description="Удаление варианта временного теста"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту ответов"),
            404: OpenApiResponse(description="Вариант ответов с данным ID не найден")
        }
    )
    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TempBlankList(APIView):
    model = TempBlank
    parent_model = TempQuiz
    serializer = TempBlankSerializer

    @extend_schema(
        tags=['Temps'],
        summary="Список работ временного теста",
        description="Получение списка работ для временного теста с pk=test_pk",
        responses={
            200: OpenApiResponse(
                response=TempBlankSerializer(many=True),
                description="Список работ временного теста"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Временный тест с данным ID не найден")
        }
    )
    def get(self, request, test_pk):
        blanks = get_object_or_404(self.parent_model, pk=test_pk).blanks
        serialized = self.serializer(blanks, many=True)
        return Response(serialized.data)

    @extend_schema(
        tags=['Temps'],
        summary="Загрузка работы для временного теста",
        description="Загрузка работы для временного теста с pk=test_pk",
        responses={
            200: OpenApiResponse(
                response=TempBlankSerializer(many=True),
                description="Проверенная работа"
            ),
            400: OpenApiResponse(description="Ошибка загрузки фото"),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Временный тест с данным ID не найден")
        }
    )
    def post(self, request, test_pk):
        quiz = get_object_or_404(self.parent_model, pk=test_pk)
        images = request.FILES.getlist('images')
        invalid_blanks = []
        without_pattern = []
        serialized_list = []
        for image in images:
            results = checker(image.temporary_file_path())
            if results == 'invalid':
                invalid_blanks.append(image.file_name)
                continue
            new_image = Image.fromarray(results.img)
            bytes_io = BytesIO()
            new_image.save(bytes_io, format='JPEG')
            file = InMemoryUploadedFile(
                bytes_io, None, 'image.jpg', 'image/jpeg',
                bytes_io.getbuffer().nbytes, None
            )
            if 0 < int(results.var) <= 10:
                var = int(results.var)
            
            blank = self.model.objects.create(
                quiz=quiz,
                var=var,
                id_blank=str(results.id),
                answers=list(results.answers.values()),
                image=file
            )
            serialized_list.append(self.serializer(blank).data)
            score = TempScore.objects.create(blank=blank)
            if var in [item.num for item in quiz.patterns.all()]:
                check_blank(score)
                serialized_list.append(self.serializer(blank).data)
            else:
                without_pattern.append(self.serializer(blank).data)
        response = {
            "blanks": serialized_list,
            "withoutPattern": without_pattern,
            "invalidBlanks": invalid_blanks
        }
        return Response(response, status=status.HTTP_201_CREATED)


class TempBlankDetail(APIView):
    model = TempBlank
    serializer = TempBlankSerializer

    @extend_schema(
        tags=['Temps'],
        summary="Работа временного теста",
        description="Получение работы для временного теста с pk=blank_pk",
        responses={
            200: OpenApiResponse(
                response=TempBlankSerializer(),
                description="Проверенная работа"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данной работе"),
            404: OpenApiResponse(description="Работа с данным ID не найдена")
        }
    )
    def get(self, request, blank_pk):
        blank = get_object_or_404(TempBlank, pk=blank_pk)
        serialized = self.serializer(blank)
        return Response(serialized.data)

    @extend_schema(
        tags=['Temps'],
        summary="Изменение работы временного теста",
        description="Изменение работы для временного теста с pk=blank_pk",
        request=TempBlankSerializer,
        responses={
            200: OpenApiResponse(
                response=TempBlankSerializer(),
                description="Проверенная работа изменена"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данной работе"),
            404: OpenApiResponse(description="Работа с данным ID не найдена")
        }
    )
    def put(self, request, blank_pk):
        blank = get_object_or_404(TempBlank, pk=blank_pk)
        serialized = self.serializer(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)

    @extend_schema(
        tags=['Temps'],
        summary="Удаление работы временного теста",
        description="Удаление работы для временного теста с pk=blank_pk",
        responses={
            204: OpenApiResponse(
                description="Работа успешно удалена"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данной работе"),
            404: OpenApiResponse(description="Работа с данным ID не найдена")
        }
    )
    def delete(self, request, blank_pk):
        blank = get_object_or_404(TempBlank, pk=blank_pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)