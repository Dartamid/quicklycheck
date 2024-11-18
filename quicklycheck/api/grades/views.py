from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.grades.models import Grade
from api.grades.serializers import GradeSerializer
from api.teachers.permissions import IsTeacher
from api.combined.serializers import GradeDetailSerializer


class GradeList(APIView):
    model = Grade
    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        teacher = self.request.user
        queryset = Grade.objects.filter(teacher=teacher)
        return queryset

    def get(self, request):
        user = request.user
        classes = self.model.objects.filter(teacher=user)
        serialized = GradeSerializer(classes, many=True)

        return Response(serialized.data)

    def post(self, request):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(teacher=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeDetail(APIView):
    model = Grade
    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        inst = self.get_object(pk)
        serialized = self.serializer_class(inst)
        return Response(serialized.data)

    def put(self, request, pk):
        inst = self.get_object(pk)
        serialized = self.serializer_class(inst, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inst = self.get_object(pk)
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
