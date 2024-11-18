from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feedback
from .serializers import FeedbackSerializer
from quicklycheck.api.blanks.models import Blank


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
