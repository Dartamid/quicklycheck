from django.urls import path
from api.tokens.views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView


urlpatterns = [
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh')
]
