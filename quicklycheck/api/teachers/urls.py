from django.urls import path, include
from .views import UserList, ProfileView, ProfileEditView, CreateUserView, ChangePasswordView

urls_users = [
    path('users/', UserList.as_view(), name='user_list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('registration/', CreateUserView.as_view(), name='register'),
    path('user/password_change/', ChangePasswordView.as_view(), name='password_change'),
]