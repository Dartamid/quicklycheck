from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UsersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='HasNoName'
        )
        self.user_admin = User.objects.create_user(
            username='AdminUser',
            is_staff=True,
            is_superuser=True,
        )
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.user_admin)

    def test_get_users_by_unauthorized(self):
        url = reverse('user_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'Вам необходимо авторизоваться для выполнения данного действия!'
        )

    def test_get_users_by_usual_user(self):
        url = reverse('user_list')
        response = self.authorized_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'У вас недостаточно прав для данного действия!')

    def test_get_users_by_admin_user(self):
        url = reverse('user_list')
        response = self.admin_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data,
            [
                {'pk': 1, 'username': 'HasNoName'},
                {'pk': 2, 'username': 'AdminUser'},
            ]
        )

    def test_normal_register(self):
        url = reverse('register')
        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
                'password': 'GKMo83Kf_y',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_object_or_404(User, email='noname@email.com')
        self.assertEqual(user.username, 'nonameemailcom')

    def test_register_with_already_registered_email(self):
        url = reverse('register')
        User.objects.create_user(username='nonameemailcom', email='noname@email.com', password='GKMo83Kf_y')
        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
                'password': 'GKMo82Kf_y',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Этот Email уже используется в системе!')

    def test_register_without_password(self):
        url = reverse('register')
        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
            }
        )
        print(response.data['detail'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Пароль обязательное поле!'
        )

    def test_register_without_email(self):
        url = reverse('register')
        response = self.guest_client.post(
            url,
            format='json',
            data={
                'password': 'GKMo83Kf_y',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Email обязательное поле!',
        )

    def test_register_with_wrong_password(self):
        url = reverse('register')
        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
                'password': '12345678',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Введённый пароль слишком широко распространён.'
        )

        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
                'password': 'abcd',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.'
        )

        response = self.guest_client.post(
            url,
            format='json',
            data={
                'email': 'noname@email.com',
                'password': '23443524524234',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Введённый пароль состоит только из цифр.'
        )


