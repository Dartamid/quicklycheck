from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.grades.models import Grade
from api.grades.serializers import GradeSerializer
from api.teachers.permissions import IsTeacher
from api.combined.serializers import GradeDetailSerializer


class GradeList(APIView):
    model = Grade
    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        teacher = self.request.user
        queryset = Grade.objects.filter(teacher=teacher)
        return queryset

    @extend_schema(
        tags=['Grades'],
        summary="Список классов",
        description="Возвращает список классов пользователя",
        request=GradeSerializer,
        responses={
            200: OpenApiResponse(
                response=GradeSerializer(many=True),
                description="Список классов"
            )
        }
    )
    def get(self, request):
        user = request.user
        classes = self.model.objects.filter(teacher=user)
        serialized = GradeSerializer(classes, many=True)

        return Response(serialized.data)

    @extend_schema(
        tags=['Grades'],
        summary="Создание нового класса",
        description="Создает новый класс к которому привязывается номер и буква",
        request=GradeSerializer,
        responses={
            201: OpenApiResponse(
                response=GradeSerializer(),
                description="Новый класс"
            ),
            400: OpenApiResponse(description="Ошибка валидации"),
        }
    )
    def post(self, request):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeDetail(APIView):
    model = Grade
    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        tags=['Grades'],
        summary="Класс по ID",
        description="Возвращает класс с данным ID",
        request=GradeSerializer,
        responses={
            200: OpenApiResponse(
                response=GradeSerializer(),
                description="Класс по ID"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному классу"),
            404: OpenApiResponse(description="Класс с данным ID не найден"),
        }
    )
    def get(self, request, pk):
        inst = self.get_object(pk)
        serialized = self.serializer_class(inst)
        return Response(serialized.data)

    @extend_schema(
        tags=['Grades'],
        summary="Изменение класса",
        description="Изменяет одно или несколько полей модели класса",
        request=GradeSerializer,
        responses={
            200: OpenApiResponse(
                response=GradeSerializer(),
                description="Измененный класс"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному классу"),
            404: OpenApiResponse(description="Класс с данным ID не найден"),
        }
    )
    def put(self, request, pk):
        inst = self.get_object(pk)
        serialized = self.serializer_class(inst, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Grades'],
        summary="Изменение класса",
        description="Изменяет одно или несколько полей модели класса",
        request=GradeSerializer,
        responses={
            204: OpenApiResponse(
                description="Класс удален"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному классу"),
            404: OpenApiResponse(description="Класс с данным ID не найден"),
        }
    )
    def delete(self, request, pk):
        inst = self.get_object(pk)
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
