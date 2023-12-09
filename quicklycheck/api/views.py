from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ClassSerializer, StudentSerializer, TestSerializer,
    PatternSerializer, BlankSerializer
)
from checker.models import (
    Class, Student, Test, Pattern, Blank
)
from checker.utils import checker
from rest_framework.permissions import IsAuthenticated
from io import BytesIO


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
    def get_object(self, pk):
        try:
            return Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        inst = self.get_object(pk)
        if inst.teacher == request.user:
            serialized = ClassSerializer(inst)
            return Response(serialized.data)
        raise Http404

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

    def get(self, request, test_pk):
        user = request.user
        patterns = get_object_or_404(Test, pk=test_pk, teacher=user).patterns
        serialized = PatternSerializer(patterns, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        serialized = PatternSerializer(data=request.data)
        test = get_object_or_404(Test, pk=test_pk, teacher=request.user)
        if serialized.is_valid():
            serialized.save(test=test)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class PatternDetail(APIView):
    serializer = PatternSerializer

    def get_object(self, patt_pk):
        try:
            return Pattern.objects.get(pk=patt_pk)
        except Pattern.DoesNotExist:
            raise Http404

    def get(self, request, patt_pk):
        pattern = self.get_object(patt_pk)
        serialized = PatternSerializer(pattern)
        if pattern.grade.teacher == request.user:
            serialized = PatternSerializer(pattern)
            return Response(serialized.data)
        raise Http404

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

    def get(self, request, class_pk):
        user = request.user
        students = get_object_or_404(Class, pk=class_pk, teacher=user).students
        serialized = StudentSerializer(students, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        serialized = StudentSerializer(data=request.data)
        grade = get_object_or_404(Class, pk=class_pk, teacher=request.user)
        if serialized.is_valid():
            serialized.save(grade=grade, teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    def get_student(self, student_pk):
        try:
            return Student.objects.get(pk=student_pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, student_pk):
        student = self.get_student(student_pk)
        if student.grade.teacher == request.user:
            serialized = StudentSerializer(student)
            return Response(serialized.data)
        raise Http404

    def put(self, request, student_pk):
        student = self.get_student(student_pk)
        serialized = StudentSerializer(student, data=request.data)
        if serialized.is_valid() and student.grade.teacher == request.user:
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_pk):
        student = self.get_student(student_pk)
        if student.grade.teacher == request.user:
            student.delete()
        raise Http404


class TestList(APIView):
    serializer_class = TestSerializer

    def get(self, request):
        tests = request.user.tests
        serialized = TestSerializer(tests, many=True)
        return Response(serialized.data)

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetail(APIView):
    serializer = TestSerializer

    def get_blank(self, test_pk):
        try:
            return Test.objects.get(pk=test_pk)
        except Test.DoesNotExist:
            raise Http404

    def get(self, request, test_pk):
        test = self.get_blank(test_pk)
        if test.teacher == request.user:
            serialized = TestSerializer(test)
            return Response(serialized.data)
        raise Http404

    def put(self, request, test_pk):
        test = self.get_blank(test_pk)
        serialized = TestSerializer(test, data=request.data)
        if serialized.is_valid() and test.teacher == request.user:
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        test = self.get_blank(test_pk)
        if test.teacher == request.user:
            test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404


class BlankList(APIView):
    serializer_class = BlankSerializer

    def get(self, request, test_pk):
        user = request.user
        blanks = get_object_or_404(Test, pk=test_pk, teacher=user).blanks
        serializer = BlankSerializer(blanks, many=True)
        return Response(serializer.data)

    def post(self, request, test_pk):
        test = get_object_or_404(Test, pk=test_pk)
        images = request.FILES.getlist('images')
        serialized_list = []
        for image in images:
            results, image = checker(image.temporary_file_path())
            bytes_io = BytesIO()
            image.save(bytes_io, format='JPEG')
            file = InMemoryUploadedFile(
                bytes_io, None, 'image.jpg', 'image/jpeg',
                bytes_io.getbuffer().nbytes, None
            )
            blank = Blank.objects.create(
                test=test,
                author=test.grade.students.all()[int(results['blank_id']) - 1],
                var=int(results['var']),
                id_blank=results['blank_id'],
                answers=','.join(results['answers'].values()),
                image=file
            )
            serialized_list.append(BlankSerializer(blank))
        return Response(serialized_list)


class BlankDetail(APIView):
    serializer_class = BlankSerializer

    def get_blank(self, blank_pk):
        try:
            return Blank.objects.get(pk=blank_pk)
        except Blank.DoesNotExist:
            raise Http404

    def get(self, request, blank_pk):
        blank = self.get_blank(blank_pk)
        test = blank.test
        if test.grade.teacher == request.user:
            serialized = BlankSerializer(blank)
            return Response(serialized.data)
        raise Http404

    def put(self, request, blank_pk):
        blank = self.get_blank(blank_pk)
        serialized = BlankSerializer(blank, data=request.data)
        test = blank.test
        if serialized.is_valid() and test.teacher == request.user:
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blank_pk):
        blank = self.get_blank(blank_pk)
        test = blank.test
        if test.teacher == request.user:
            blank.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404
