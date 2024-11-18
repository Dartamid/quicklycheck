
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



