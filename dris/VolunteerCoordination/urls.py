from django.urls import path
from .views import  *
app_name = "volunteer"

urlpatterns = [
   path('volunteer-tasks/list', VolunteerTaskView.as_view(), name='task_list'),
   path('volunteer-task/<int:task_id>/volunteers/', VolunteerListByTaskSkillView.as_view(), name='volunteer_list_by_task'),
   path(
        'volunteer-task/<int:task_id>/assign/<int:volunteer_id>/',
        AssignVolunteerToTaskView.as_view(),
        name='assign_volunteer_to_task'
    ),
]