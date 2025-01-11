from rest_framework.views import APIView
from api.grades.models import Grade
from rest_framework.generics import get_object_or_404
from api.teachers.permissions import IsTeacher
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


period_choices = {
    'mouth': '%d.%m',
    'year': '%m'
}


class GradeStatsByPeriodView(APIView):
    model = Grade
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self, request):
        return self.model.objects.filter(teacher=request.user).all()

    def get_object(self, request, grade_pk):
        obj = get_object_or_404(self.get_queryset(request), pk=grade_pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, grade_pk, period='mouth'):
        grade = self.get_object(request, grade_pk)
        blanks = grade.get_blanks()
        if 'period' in request.query_params.keys():
            period = request.query_params['period']
        else:
            period = 'mouth'

        data = {}

        for blank in blanks:
            date = blank.created_at.strftime(period_choices[period])
            if date in data.keys():
                data[date].append(int(blank.score.percentage))
            else:
                data[date] = [int(blank.score.percentage)]

        for key in data.keys():
            data[key] = sum(data[key]) / len(data[key])

        return Response(data, status=status.HTTP_200_OK)