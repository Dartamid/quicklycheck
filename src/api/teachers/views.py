from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import UserSerializer, ChangePasswordSerializer, CreateUserSerializer, ProfileSerializer, AccountSerializer

User = get_user_model()


class UserList(APIView):
    model = User
    serializer_class = UserSerializer
    # creation_form = CustomUserCreationForm

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

    def post(self, request):
        account = self.get_account(request)
        serialized = self.serializer_class(account, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)

        return Response(
            data={'detail': 'Успешная регистрация пользователя!'},
            status=status.HTTP_201_CREATED,
        )

        # def post(self, request):
    #
    #     form = self.creation_form(request.data)
    #
    #     if form.is_valid():
    #         email = form.cleaned_data.get('email')
    #         if len(User.objects.filter(email=email)) == 0:
    #             username = email.replace('@', '', 1)
    #             password = form.cleaned_data.get('password1')
    #             user = User.objects.create_user(username, email, password)
    #             user.save()
    #             return Response(data={'detail': 'Успешная регистрация пользователя'}, status=status.HTTP_201_CREATED)
    #         return Response(
    #             data={'detail': 'Данный Email уже используется в системе!'},
    #             status=status.HTTP_400_BAD_REQUEST, exception=True
    #         )
    #     return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serialized = self.get_serializer(data=request.data)

        if serialized.is_valid():
            if not obj.check_password(serialized.data.get("old_password")):
                return Response({"detail": 'Текущий пароль введен неверно!'}, status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serialized.data.get("new_password"))
            obj.save()

            return Response('Установлен новый пароль!', status=status.HTTP_200_OK)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)