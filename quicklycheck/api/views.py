from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import (
    AssessmentSerializer, ClassSerializer, StudentSerializer, StudentDetailSerializer, TestSerializer,
    PatternSerializer, BlankSerializer, TempTestSerializer, TempPatternSerializer,
    TempBlankSerializer, FeedbackSerializer,
)

from checker.models import (
    Assessment, Class, Student, Test, Pattern, Blank, TempTest, TempPattern, TempBlank
)
from .models import Feedback
from checker.utils import checker
from rest_framework.permissions import IsAuthenticated
from io import BytesIO
from PIL import Image
from checker.models import User
from .teachers.serializers import CreateUserSerializer

from .teachers.models import Account

from .teachers.serializers import ChangePasswordSerializer


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.teacher == request.user:
            return True


class ClassList(APIView):
    model = Class
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        teacher = self.request.user
        queryset = Class.objects.filter(teacher=teacher)
        return queryset

    def get(self, request):
        user = request.user
        classes = self.model.objects.filter(teacher=user)
        serialized = ClassSerializer(classes, many=True)

        return Response(serialized.data)

    def post(self, request):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassDetail(APIView):
    model = Class
    serializer = ClassSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        inst = self.get_object(pk)
        serialized = self.serializer(inst)
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
    serializer = PatternSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, test_pk):
        user = request.user
        patterns = get_object_or_404(Test, pk=test_pk, teacher=user).patterns
        serialized = self.serializer(patterns, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        test = get_object_or_404(Test, pk=test_pk, teacher=request.user)
        data = request.data.copy()
        data['test'] = test.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
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
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern)
        return Response(serialized.data)

    def put(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentList(APIView):
    model = Student
    serializer = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, class_pk):
        user = request.user
        students = get_object_or_404(Class, pk=class_pk, teacher=user).students
        serialized = self.serializer(students, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        grade = get_object_or_404(Class, pk=class_pk, teacher=request.user)
        data = request.data.copy()
        data['grade'] = grade.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    model = Student
    serializer = StudentDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, student_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["student_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = self.serializer(student)
        return Response(serialized.data)

    def put(self, request, student_pk):
        student = self.get_object(student_pk)
        serialized = self.serializer(student, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_pk):
        student = self.get_object(student_pk)
        student.delete()
        return Response(data={'detail': 'Ученик удален!'}, status=status.HTTP_204_NO_CONTENT)


class TestList(APIView):
    model = Class
    serializer = TestSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, class_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["class_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, class_pk):
        grade = self.get_object(class_pk)
        tests = grade.tests
        serialized = self.serializer(tests, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        data = request.data.copy()
        data['teacher'] = request.user
        data['grade'] = self.get_object(class_pk).pk
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetail(APIView):
    model = Test
    serializer = TestSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = self.serializer(test)
        return Response(serialized.data)

    def put(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = self.serializer(test, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        test = self.get_object(test_pk)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssessmentList(APIView):
    model = Assessment
    parent_model = Test
    serializer = AssessmentSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.parent_model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=test_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        assessments = self.get_object(test_pk).assessments
        serialized = self.serializer(assessments, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        data = request.data.copy()
        data['test_pk'] = test_pk
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentDetail(APIView):
    model = Assessment
    serializer = AssessmentSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, pk):
        assessment = self.get_object(pk)
        serialized = self.serializer(assessment)
        return Response(serialized.data)

    def put(self, request, pk):
        assessment = self.get_object(pk)
        serialized = self.serializer(assessment, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        assessment = self.get_object(test_pk)
        assessment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlankList(APIView):
    model = Test
    serializer = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        blanks = self.get_object(test_pk).blanks
        serializer = self.serializer(blanks, many=True)
        return Response(serializer.data)

    def post(self, request, test_pk):
        test = self.get_object(test_pk)
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
            if len(test.grade.students.all()) >= int(results.id) - 1:
                author = test.grade.students.all()[int(results.id) - 1]
            else:
                author = test.grade.students.all()[1]
            if int(results.var) in [item.num for item in test.patterns.all()]:
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
            serialized_list.append(self.serializer(blank).data)
        return Response(serialized_list, status=status.HTTP_201_CREATED)


class BlankDetail(APIView):
    model = Blank
    serializer = BlankSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, pk):
        blank = self.get_object(pk)
        serialized = self.serializer(blank)
        return Response(serialized.data)

    def put(self, request, pk):
        blank = self.get_object(pk)
        serialized = self.serializer(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blank = self.get_object(pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TempTestList(APIView):
    model = TempTest
    serializer = TempTestSerializer

    def post(self, request):
        test = self.model.objects.create()
        serialized = self.serializer(test)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class TempPatternList(APIView):
    model = TempPattern
    serializer = TempPatternSerializer

    def get(self, request, test_pk):
        test = get_object_or_404(TempTest, pk=test_pk)
        tests = self.model.objects.filter(test=test)
        serialized = self.serializer(tests, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, test_pk):
        test = get_object_or_404(TempTest, pk=test_pk)
        data = request.data.copy()
        data['test'] = test.pk
        serialized = self.serializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class TempPatternDetail(APIView):
    model = TempPattern
    serializer = TempPatternSerializer

    def get_object(self, patt_pk):
        try:
            return self.model.objects.get(pk=patt_pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = self.serializer(pattern, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TempBlankList(APIView):
    model = TempBlank
    parent_model = TempTest
    serializer = TempBlankSerializer

    def get(self, request, test_pk):
        blanks = get_object_or_404(self.parent_model, pk=test_pk).blanks
        serialized = self.serializer(blanks, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        test = get_object_or_404(self.parent_model, pk=test_pk)
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
            blank = self.model.objects.create(
                test=test,
                var=var,
                id_blank=str(results.id),
                answers=str(','.join(results.answers.values())),
                image=file
            )
            serialized_list.append(self.serializer(blank).data)
        return Response(serialized_list)


class TempBlankDetail(APIView):
    model = TempBlank
    serializer = TempBlankSerializer

    def get_blank(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blank = self.get_blank(pk)
        serialized = self.serializer(blank)
        return Response(serialized.data)

    def put(self, request, pk):
        blank = self.get_blank(pk)
        serialized = self.serializer(blank, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)

    def delete(self, request, pk):
        blank = self.get_blank(pk)
        blank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedBackView(APIView):
    model = Feedback
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        data = request.data.copy()
        blank = get_object_or_404(Blank, pk=data['blank'], teacher=request.user)
        data['blank'] = blank
        serialized = self.serializer_class(data=data)
        if serialized.is_valid():
            serialized.save(user=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
