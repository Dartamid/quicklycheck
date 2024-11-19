from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.tokens.serializers import TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        tags=['Tokens'],
        summary="Получение токенов авторизации",
        description="Возвращает два токена Access и Refresh, которые нужны для авторизации запросов API. "
                    "Длительность жизни токенов 5 мин для Access и 365 дней для Refresh токена.",
        responses={
            200: OpenApiResponse(
                response=TokenObtainPairResponseSerializer(),
                description="Список вариантов"
            ),
            403: OpenApiResponse(description="У вас нет доступа к данному тесту"),
            404: OpenApiResponse(description="Тест с данным ID не найден")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        tags=['Tokens'],
        summary="Обновление токена авторизации",
        description="Возвращает обновленный Access токен.",
        responses={
            200: OpenApiResponse(
                response=TokenRefreshResponseSerializer(),
                description="Обновленный Access токен"
            ),
            400: OpenApiResponse(description="Refresh токен не был предоставлен"),
            403: OpenApiResponse(description="Введен неверный Refresh токен")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)