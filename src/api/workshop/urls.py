from django.urls import path

from api.workshop.views import WorkshopList, WorkshopQuizPublish

urlpatterns = [
    path('workshop/', WorkshopList.as_view(), name='workshop'),
    path('workshop/public/<int:quiz_pk>/', WorkshopQuizPublish.as_view(), name='workshop_publish')
]