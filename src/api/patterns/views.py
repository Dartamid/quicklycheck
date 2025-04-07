from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .serializers import PatternSerializer, QuestionSerializer, AnswerChoiceSerializer
from api.teachers.permissions import IsTeacher
from api.patterns.models import Pattern, Question, AnswerChoice
from api.quizzes.models import Quiz
from api.blanks.views import check_blank


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
        quiz = get_object_or_404(Quiz, pk=test_pk, teacher=request.user)
        data = request.data.copy()
        data['quiz'] = quiz.pk
        data['teacher'] = quiz.teacher.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            blanks_with_this_pattern = quiz.without_pattern_blanks().filter(var=data['num'])
            if blanks_with_this_pattern.count() > 0:
                for blank in blanks_with_this_pattern:
                    check_blank(blank.score)
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
        self.check_object_permissions(self.request, obj.quiz)
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
            blanks = pattern.quiz.blanks.filter(var=pattern.num)
            for blank in blanks:
                check_blank(blank.score)
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


class QuestionList(APIView):
    model = Question
    serializer = QuestionSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


    @extend_schema(
        tags=['Patterns'],
        summary="Создание нового вопроса",
        description="Создает новый вопрос для варианта теста с ID <pk>. Вопрос содержит в себе свой номер, а также текст и варианты"
        "ответов на вопросы в тесте.",
        request=QuestionSerializer,
        responses={
            200: OpenApiResponse(
                response=QuestionSerializer(),
                description="Вопрос успешно создан"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному варианту"),
            404: OpenApiResponse(description="Вариант с данным ID не найден")
        }
    )
    def post(self, request, pattern_pk):
        pattern = get_object_or_404(Pattern, pk=pattern_pk, teacher=request.user)
        data = request.data.copy()
        data['pattern'] = pattern.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            blanks_with_this_pattern = pattern.quiz.without_pattern_blanks().filter(var=data['num'])
            if blanks_with_this_pattern.count() > 0:
                for blank in blanks_with_this_pattern:
                    check_blank(blank.score)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    model = Question
    serializer = QuestionSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    @extend_schema(
        tags=['Patterns'],
        summary="Детализация вопроса",
        description="Получение вопроса по ID <pk>",
        responses={
            200: OpenApiResponse(
                response=QuestionSerializer(),
                description="Вопрос"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному вопросу"),
            404: OpenApiResponse(description="Вопрос с данным ID не найден")
        }
    )
    def get(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk, pattern__teacher=request.user)
        serialized = self.serializer(question)
        return Response(serialized.data)

    @extend_schema(
        tags=['Patterns'],
        summary="Изменение вопроса",
        description="Изменяет одно или несколько полей в модели вопроса с ID <pk>.",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=QuestionSerializer(),
                description="Вопрос"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному вопросу"),
            404: OpenApiResponse(description="Вопрос с данным ID не найден")
        }
    )
    def put(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk, pattern__teacher=request.user)
        serialized = self.serializer(question_pk, data=request.data)
        pattern = question.pattern
        if serialized.is_valid():
            serialized.save()
            blanks = pattern.quiz.blanks.filter(var=pattern.num)
            for blank in blanks:
                check_blank(blank.score)
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Patterns'],
        summary="Удаление вопроса",
        description="Удаление вопроса с ID <pk>.",
        request=PatternSerializer,
        responses={
            204: OpenApiResponse(
                description="Вопроса удален"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному вопросу"),
            404: OpenApiResponse(description="Вопрос с данным ID не найден")
        }
    )
    def delete(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk, pattern__teacher=request.user)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerChoiceList(APIView):
    model = AnswerChoice
    serializer = AnswerChoiceSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


    @extend_schema(
        tags=['Patterns'],
        summary="Список вариантов ответов на вопрос",
        description="Возвращает список вариантов ответов для вопроса с ID <question_pk>",
        responses={
            200: OpenApiResponse(
                response=AnswerChoiceSerializer(many=True),
                description="Список вариантов ответов"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному вопросу"),
            404: OpenApiResponse(description="Вопрос с данным ID не найден")
        }
    )
    def get(self, request, question_pk):
        user = request.user
        choices = get_object_or_404(Question, pk=question_pk, teacher=user).answer_choices
        serialized = self.serializer(choices, many=True)
        return Response(serialized.data)


    @extend_schema(
        tags=['Patterns'],
        summary="Создание нового варианта ответа",
        description="Создает новый вариант ответа для вопрсоа с ID <question>. Ответ содержит в себе свой порядковый номер,"
        "а также текст",
        request=QuestionSerializer,
        responses={
            200: OpenApiResponse(
                response=QuestionSerializer(),
                description="Вариант ответа успешно создан"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному вопросу"),
            404: OpenApiResponse(description="Вопрос с данным ID не найден")
        }
    )
    def post(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk, pattern__teacher=request.user)
        pattern = question.pattern
        data = request.data.copy()
        data['question'] = question.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            blanks_with_this_pattern = pattern.quiz.without_pattern_blanks().filter(var=data['num'])
            if blanks_with_this_pattern.count() > 0:
                for blank in blanks_with_this_pattern:
                    check_blank(blank.score)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerChoicesDetail(APIView):
    model = AnswerChoice
    serializer = AnswerChoiceSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    @extend_schema(
        tags=['Patterns'],
        summary="Детализация варианта ответа на вопрос",
        description="Получение варианта ответа на вопрос по ID <pk>",
        responses={
            200: OpenApiResponse(
                response=AnswerChoiceSerializer(),
                description="Вариант ответа на вопрос"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному объекту"),
            404: OpenApiResponse(description="Объект с данным ID не найден")
        }
    )
    def get(self, request, answer_pk):
        question = get_object_or_404(AnswerChoice, pk=answer_pk)
        serialized = self.serializer(question)
        return Response(serialized.data)

    @extend_schema(
        tags=['Patterns'],
        summary="Изменение варианта ответа на вопрос",
        description="Изменяет одно или несколько полей в модели варианта ответа на вопрос с ID <pk>.",
        request=PatternSerializer,
        responses={
            200: OpenApiResponse(
                response=AnswerChoiceSerializer(),
                description="Вариант ответа на вопрос"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному объекту"),
            404: OpenApiResponse(description="Объект с данным ID не найден")
        }
    )
    def put(self, request, answer_pk):
        answer = get_object_or_404(AnswerChoice, pk=answer_pk)
        serialized = self.serializer(answer, data=request.data)
        pattern = answer.question.pattern
        if serialized.is_valid():
            serialized.save()
            blanks = pattern.quiz.blanks.filter(var=pattern.num)
            for blank in blanks:
                check_blank(blank.score)
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Patterns'],
        summary="Удаление варианта ответа на вопрос",
        description="Удаление вариана ответа на вопрос с ID <pk>.",
        responses={
            204: OpenApiResponse(
                description="Вариант ответа на вопрос удален"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному объекту"),
            404: OpenApiResponse(description="Объект с данным ID не найден")
        }
    )
    def delete(self, request, answer_pk):
        answer = get_object_or_404(AnswerChoice, pk=answer_pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)