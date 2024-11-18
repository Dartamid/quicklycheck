from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .serializers import PatternSerializer


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