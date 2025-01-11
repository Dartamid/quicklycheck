from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from checker.utils import checker
from api.quizzes.models import Quiz
from api.teachers.permissions import IsTeacher
from api.blanks.serializers import BlankSerializer
from api.blanks.models import Blank, Score


def check_blank(score):
    pattern = score.blank.quiz.patterns.filter(num=score.blank.var)[0].split(',')
    checked_answers = {}
    right=0
    for key in range(len(pattern)):
        is_right = True if pattern[key] == score.blank.answers[str(key)] else False
        right += 1 if is_right else 0
        checked_answers[str(key)] = {
            'actual': score.blank.answers[str(key)],
            'correct': pattern[key],
            'isRight': is_right,
        }
    score.percentage = right/len(pattern)
    score.total=len(pattern)
    score.right=right
    score.is_checked=True
    score.checked_answers=checked_answers


class BlankList(APIView):
    model = Quiz
    serializer_class = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, quiz_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["quiz_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        tags=['Blanks'],
        summary="Список выполненных работ",
        description="Возвращает список выполненных работ  для Теста с ID <pk>",
        responses={
            200: OpenApiResponse(
                response=BlankSerializer(many=True),
                description="Список вариантов оценивания"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def get(self, request, quiz_pk):
        blanks = self.get_object(quiz_pk).blanks
        serializer = self.serializer_class(blanks, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Blanks'],
        summary="Загрузка новой работы",
        description="Загрузка работы на проверку для Теста с ID <pk>",
        responses={
            200: OpenApiResponse(
                response=BlankSerializer(),
                description="Проверенная работа"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def post(self, request, quiz_pk):
        quiz = self.get_object(quiz_pk)
        images = request.FILES.getlist('images')
        serialized_list = []
        for image in images:
            results = checker(image.temporary_file_path())
            new_image = Image.fromarray(results.img)
            bytes_io = BytesIO()
            new_image.save(bytes_io, format='JPEG')
            file = InMemoryUploadedFile(
                bytes_io, None, 'image.jpg', 'image/jpeg',
                bytes_io.getbuffer().nbytes, None
            )
            if len(quiz.grade.students.all()) >= int(results.id) - 1:
                author = quiz.grade.students.all()[int(results.id) - 1]
            else:
                author = quiz.grade.students.all()[1]
            # if int(results.var) in [item.num for item in quiz.patterns.all()]:
            #     var = int(results.var)
                
            # else:
            #     if len(quiz.patterns.all()) > 0:
            #         var = quiz.patterns.all()[0].num
            #     else:
            #         return Response('У данного теста не найдены варианты!', status=status.HTTP_400_BAD_REQUEST)
            if 0 < int(results.var) <= 10:
                var = int(results.var)
            blank = Blank.objects.create(
                quiz=quiz,
                author=author,
                var=var,
                id_blank=str(results.id),
                answers=list(results.answers.values()),
                image=file
            )
            score = Score.objects.create(blank=blank)
            if var in [item.num for item in quiz.patterns.all()]:
                check_blank(score)
            serialized_list.append(self.serializer_class(blank).data)
        return Response(serialized_list, status=status.HTTP_201_CREATED)


class BlankDetail(APIView):
    model = Blank
    serializer_class = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj.quiz)
        return obj

    @extend_schema(
        tags=['Blanks'],
        summary="Проверенная работа",
        description="Вовращает проверенную на работу по ID",
        responses={
            200: OpenApiResponse(
                response=BlankSerializer(),
                description="Проверенная работа"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def get(self, request, pk):
        blank = self.get_object(pk)
        serialized = self.serializer_class(blank)
        return Response(serialized.data)

    @extend_schema(
        tags=['Blanks'],
        summary="Изменение проверенной работы",
        description="Изменяет одно или несколько полей проверенной работы",
        request=BlankSerializer(),
        responses={
            200: OpenApiResponse(
                response=BlankSerializer(),
                description="Измененная работа"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def put(self, request, pk):
        blank = self.get_object(pk)
        serialized = self.serializer_class(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Blanks'],
        summary="Удаление работы",
        description="Удаляет из базы данных работу по ID",
        request=BlankSerializer(),
        responses={
            204: OpenApiResponse(
                description="Работа удалена"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def delete(self, request, pk):
        blank = self.get_object(pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
