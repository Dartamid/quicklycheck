from rest_framework.views import APIView
from api.grades.models import Grade
from api.quizzes.models import Quiz
from rest_framework.generics import get_object_or_404
from api.teachers.permissions import IsTeacher
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


period_choices = [
    '%d.%m.%Y',
    '%m.%y'
]


class GradeStatsByPeriodView(APIView):
    model = Grade
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self, request):
        return self.model.objects.filter(teacher=request.user).all()

    def get_object(self, request, grade_pk):
        obj = get_object_or_404(self.get_queryset(request), pk=grade_pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, grade_pk):
        grade = self.get_object(request, grade_pk)
        blanks = grade.get_blanks()
        if 'period' in request.query_params.keys():
            per = request.query_params['period']
        else:
            per = 0

        raw_data = {}

        for blank in blanks:
            date = blank.created_at.strftime(period_choices[per])
            if date in raw_data.keys():
                raw_data[date].append(int(blank.score.percentage))
            else:
                raw_data[date] = [int(blank.score.percentage)]

        clear_data = {
            "stats": [],
        }

        for key in raw_data.keys():
            clear_data['stats'].append({
                "date": key,
                "avg": sum(raw_data[key]) / len(raw_data[key])
            })

        return Response(clear_data, status=status.HTTP_200_OK)
    

class QuizGraphsView(APIView):
    model = Quiz
    permission_classes = (IsAuthenticated, IsTeacher)

    def get_queryset(self, request):
        return self.model.objects.filter(teacher=request.user).all()

    def get_object(self, request, quiz_pk):
        obj = get_object_or_404(self.get_queryset(request), pk=quiz_pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, quiz_pk):
        quiz = self.get_object(request, quiz_pk)
        blanks = quiz.valid_blanks()

        raw_data = {}
        clear_data = {}
        if len(blanks) > 0:
            for blank in blanks:
                for i, answer in enumerate(blank.score.checked_answers):
                    if i in raw_data.keys():
                        raw_data[str(i)] += 1 if answer['isRight'] else 0
                    else:
                        raw_data[str(i)] = 1 if answer['isRight'] else 0

            most_hard = min(list(raw_data.items()), key=lambda x: x[1])
            check = list(raw_data.values())
            clear_data["questions"] = [item / len(blanks) * 100 for item in raw_data.values()],
            clear_data["mostHard"] = most_hard[0]
        
        return Response(clear_data, status=status.HTTP_200_OK)