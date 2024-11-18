from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.grades.models import Grade
from api.teachers.permissions import IsTeacher
from api.quizzes.models import Quiz
from api.quizzes.serializers import QuizSerializer


class QuizList(APIView):
    model = Grade
    serializer_class = QuizSerializer
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
        serialized = self.serializer_class(tests, many=True)
        return Response(serialized.data)

    def post(self, request, class_pk):
        data = request.data.copy()
        data['teacher'] = request.user
        data['grade'] = self.get_object(class_pk).pk
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetail(APIView):
    model = Quiz
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, test_pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["test_pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = self.serializer_class(test)
        return Response(serialized.data)

    def put(self, request, test_pk):
        test = self.get_object(test_pk)
        serialized = self.serializer_class(test, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, test_pk):
        test = self.get_object(test_pk)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
