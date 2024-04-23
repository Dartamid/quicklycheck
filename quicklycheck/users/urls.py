from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import SignUpView
 
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
