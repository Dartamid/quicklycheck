from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import UserSerializer, ChangePasswordSerializer, CreateUserSerializer, ProfileSerializer, \
    AccountSerializer

User = get_user_model()


class UserList(APIView):
    model = User
    serializer_class = UserSerializer

    @extend_schema(
        tags=['Teachers'],
        summary="Список учителей",
        description="Возвращает список учителей. Запрос доступен только для администрации сайта",
        responses={
            200: OpenApiResponse(
                response=UserSerializer(many=True),
                description="Список учителей",
            ),
            403: OpenApiResponse(
                description="У вас нет доступа к данному запросу",
            )
        }
    )
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                users = self.model.objects.all()
                serialized = self.serializer_class(users, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={'detail': 'У вас недостаточно прав для данного действия!'}
                )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'detail': 'Вам необходимо авторизоваться для выполнения данного действия!'}
            )


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    @extend_schema(
        tags=['Teachers'],
        summary="Профиль учителя",
        description="Возвращает данные профиля учителя",
        responses={
            200: OpenApiResponse(
                response=ProfileSerializer(),
                description="Профиль учителя",
            ),
            403: OpenApiResponse(
                description="Для данного запроса необходимо авторизоваться",
            )
        }
    )
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)


class ProfileEditView(APIView):
    permission_classes = (IsAuthenticated,)
    model = Account
    serializer_class = AccountSerializer

    def get_account(self, request):
        user = get_object_or_404(self.model, user=request.user.id)
        return user

    @extend_schema(
        tags=['Teachers'],
        summary="Изменение данных учителя",
        description="Изменяет одно или несколько полей данных профиля учителя",
        request=AccountSerializer,
        responses={
            200: OpenApiResponse(
                response=ProfileSerializer(),
                description="Профиль учителя",
            ),
            403: OpenApiResponse(
                description="Для данного запроса необходимо авторизоваться",
            )
        }
    )
    def post(self, request):
        account = self.get_account(request)
        serialized = self.serializer_class(account, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    @extend_schema(
        tags=['Users'],
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email, именем, фамилией. "
                    "Возраст должен быть в пределах от 16 до 99 лет.",
        request=CreateUserSerializer,
        examples=[
            OpenApiExample(
                'Registration Data',
                {'email': 'example@example.com','password': 'password123'},
                request_only=True
            ),
        ],
        responses={
            201: OpenApiResponse(
                response={'detail': 'Успешная регистрация пользователя!'},
                description="Пользователь успешно создан",
            ),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request, *args, **kwargs):
        user = self.create(request, *args, **kwargs)
        Account.objects.create(user=user)
        return Response(
            data={'detail': 'Успешная регистрация пользователя!'},
            status=status.HTTP_201_CREATED,
        )


class ChangePasswordView(APIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def get_user(self, queryset=None):
        obj = self.request.user
        return obj

    @extend_schema(
        tags=['Users'],
        summary="Изменение пароля пользователя",
        description="Изменяет пароль пользователя. Пароль должен содержать буквы латинского алфавита, цифры, "
                    " не должен находиться в списке \"простых\" паролей.",
        request=CreateUserSerializer,
        examples=[
            OpenApiExample(
                'Change password Data',
                {'old_password': 'oldpassword123', 'new_password': 'newpassword123'}
            ),
        ],
        responses={
            200: OpenApiResponse(
                response={'detail': 'Установлен новый пароль!'},
                description="Пароль успешно изменен"
            ),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def patch(self, request, *args, **kwargs):
        obj = self.get_user()
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():
            if not obj.check_password(serialized.data.get("old_password")):
                return Response({"detail": 'Текущий пароль введен неверно!'}, status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serialized.data.get("new_password"))
            obj.save()

            return Response('Установлен новый пароль!', status=status.HTTP_200_OK)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
