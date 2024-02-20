from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ClassSerializer, StudentSerializer, TestSerializer,
    PatternSerializer, BlankSerializer, UserSerializer, TempTestSerializer, TempPatternSerializer,
    ChangePasswordSerializer, TempBlankSerializer
)
from checker.models import (
    Class, Student, Test, Pattern, Blank, TempTest, TempPattern, TempBlank
)
from checker.utils import checker
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from io import BytesIO
from PIL import Image
from pillow_heif import register_heif_opener
from checker.models import User
from users.forms import CustomUserCreationForm


register_heif_opener()

class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.teacher == request.user:
            return True


class ClassList(APIView):
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        teacher = self.request.user
        queryset = Class.objects.filter(teacher=teacher)
        return queryset

    def get(self, request):
        user = request.user
        classes = Class.objects.filter(teacher=user)
        serialized = ClassSerializer(classes, many=True)

        return Response(serialized.data)

    def post(self, request):
        serialized = ClassSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassDetail(APIView):
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Class.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        inst = self.get_object(pk)
        serialized = ClassSerializer(inst)
        return Response(serialized.data)

    def put(self, request, pk):
        inst = self.get_object(pk)
        serialized = ClassSerializer(inst, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inst = self.get_object(pk)
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatternList(APIView):
    serializer_class = PatternSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, test_pk):
        user = request.user
        patterns = get_object_or_404(Test, pk=test_pk, teacher=user).patterns
        serialized = PatternSerializer(patterns, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        test = get_object_or_404(Test, pk=test_pk, teacher=request.user)
        data = request.data.copy()
        data['test'] = test.pk
        serialized = PatternSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class PatternDetail(APIView):
    serializer = PatternSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Pattern.objects.all()

    def get_object(self, patt_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["patt_pk"])
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = PatternSerializer(pattern)
        return Response(serialized.data)

    def put(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = PatternSerializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentList(APIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, class_pk):
        user = request.user
        students = get_object_or_404(Class, pk=class_pk, teacher=user).students
        serialized = StudentSerializer(students, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        grade = get_object_or_404(Class, pk=class_pk, teacher=request.user)
        data = request.data.copy()
        data['grade'] = grade.pk
        serialized = StudentSerializer(data=data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Student.objects.all()

    def get_object(self, student_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["student_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = StudentSerializer(student)
        return Response(serialized.data)

    def put(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = StudentSerializer(student, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_pk):
        student = self.get_object(student_pk)
        student.delete()
        return Response(data={'detail': 'Ученик удален!'}, status=status.HTTP_204_NO_CONTENT)


class TestList(APIView):
    serializer_class = TestSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Class.objects.all()

    def get_object(self, class_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["class_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, class_pk):
        grade = self.get_object(class_pk)
        tests = grade.tests
        serialized = TestSerializer(tests, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        data = request.data.copy()
        data['teacher'] = request.user
        data['grade'] = self.get_object(class_pk).pk
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetail(APIView):
    serializer = TestSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Test.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = TestSerializer(test)
        return Response(serialized.data)

    def put(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = TestSerializer(test, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        test = self.get_object(test_pk)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlankList(APIView):
    serializer_class = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Test.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        blanks = self.get_object(test_pk).blanks
        serializer = BlankSerializer(blanks, many=True)
        return Response(serializer.data)

    def post(self, request, test_pk):
        test = self.get_object(test_pk)
        images = request.FILES.getlist('images')
        serialized_list = []
        for image in images:
            pil_image = Image.open(image.temporary_file_path())
            results = checker(pil_image)
            new_image = Image.fromarray(results.img)
            bytes_io = BytesIO()
            new_image.save(bytes_io, format='JPEG')
            file = InMemoryUploadedFile(
                bytes_io, None, 'image.jpg', 'image/jpeg',
                bytes_io.getbuffer().nbytes, None
            )
            if len(test.grade.students.all()) >= int(results.id) - 1:
                author = test.grade.students.all()[int(results.id) - 1]
            else:
                author = test.grade.students.all()[1]
            if results.var in [str(item.num) for item in test.patterns.all()]:
                var = int(results.var)
            else:
                if len(test.patterns.all()) > 0:
                    var = test.patterns.all()[0].num
                else:
                    return Response('У данного теста не найдены варианты!', status=status.HTTP_400_BAD_REQUEST)
            blank = Blank.objects.create(
                test=test,
                author=author,
                var=var,
                id_blank=str(results.id),
                answers=str(','.join(results.answers.values())),
                image=file
            )
            serialized_list.append(BlankSerializer(blank).data)
        return Response(serialized_list, status=status.HTTP_201_CREATED)


class BlankDetail(APIView):
    serializer_class = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Blank.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, pk):
        blank = self.get_object(pk)
        serialized = BlankSerializer(blank)
        return Response(serialized.data)

    def put(self, request, pk):
        blank = self.get_object(pk)
        serialized = BlankSerializer(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blank = self.get_object(pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):

    def get(self, request):
        if request.user.is_admin:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer)
        else:
            return HttpResponseForbidden()

    def post(self, request):

        form = CustomUserCreationForm(request.data)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            if len(User.objects.filter(email=email)) == 0:
                username = email.replace('@', '', 1)
                password = form.cleaned_data.get('password1')
                user = User.objects.create_user(username, email, password)
                user.save()
                return Response(data={'detail': 'Успешная регистрация пользователя'}, status=status.HTTP_201_CREATED)
            return Response(data={'detail': 'Данный Email уже используется в системе!'}, status=status.HTTP_400_BAD_REQUEST, exception=True)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class TempTestList(APIView):
    serializer_class = TempTestSerializer

    def post(self, request):
        test = TempTest.objects.create()
        serializer = TempTestSerializer(test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TempPatternList(APIView):

    def get(self, request, test_pk):
        test = get_object_or_404(TempTest, pk=test_pk)
        tests = TempPattern.objects.filter(test=test)
        serializer = TempPatternSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, test_pk):
        test = get_object_or_404(TempTest, pk=test_pk)
        data = request.data.copy()
        data['test'] = test.pk
        serializer = TempPatternSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempPatternDetail(APIView):
    @staticmethod
    def get_object(patt_pk):
        try:
            return TempPattern.objects.get(pk=patt_pk)
        except TempPattern.DoesNotExist:
            raise Http404

    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = TempPatternSerializer(pattern)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = TempPatternSerializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TempBlankList(APIView):
    def get(self, request, test_pk):
        blanks = get_object_or_404(TempTest, pk=test_pk).blanks
        serializer = TempBlankSerializer(blanks, many=True)
        return Response(serializer.data)

    def post(self, request, test_pk):
        test = get_object_or_404(TempTest, pk=test_pk)
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
            if int(results.var) in [item.num for item in test.patterns.all()]:
                var = int(results.var)
            else:
                if len(test.patterns.all()) > 0:
                    var = test.patterns.all()[0].num
                else:
                    return Response('У данного теста не найдены варианты!', status=status.HTTP_400_BAD_REQUEST)
            blank = TempBlank.objects.create(
                test=test,
                var=var,
                id_blank=str(results.id),
                answers=str(','.join(results.answers.values())),
                image=file
            )
            serialized_list.append(TempBlankSerializer(blank).data)
        return Response(serialized_list)


class TempBlankDetail(APIView):

    def get_blank(self, pk):
        try:
            return TempBlank.objects.get(pk=pk)
        except TempBlank.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blank = self.get_blank(pk)
        serialized = TempBlankSerializer(blank)
        return Response(serialized.data)

    def put(self, request, pk):
        blank = self.get_blank(pk)
        serialized = TempBlankSerializer(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)

    def delete(self, request, pk):
        blank = self.get_blank(pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"detail": "Введен не правильный пароль"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
