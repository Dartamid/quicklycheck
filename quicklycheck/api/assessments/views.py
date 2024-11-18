from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Assessment
from .serializers import AssessmentSerializer
from ..quizzes.models import Quiz
from ..teachers.permissions import IsTeacher


class AssessmentList(APIView):
    model = Assessment
    parent_model = Quiz
    serializer_class = AssessmentSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.parent_model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=test_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        assessments = self.get_object(test_pk).assessments
        serialized = self.serializer_class(assessments, many=True)
        return Response(serialized.data)

    def post(self, request, test_pk):
        data = request.data.copy()
        data['test_pk'] = test_pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentDetail(APIView):
    model = Assessment
    serializer_class = AssessmentSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj.test)
        return obj

    def get(self, request, pk):
        assessment = self.get_object(pk)
        serialized = self.serializer_class(assessment)
        return Response(serialized.data)

    def put(self, request, pk):
        assessment = self.get_object(pk)
        serialized = self.serializer_class(assessment, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        assessment = self.get_object(test_pk)
        assessment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
