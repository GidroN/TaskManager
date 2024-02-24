from django.urls import path
from .views import *

urlpatterns = [
    path('', get_today_tasks, name='today_tasks'),
    path('groups/<int:group_id>/', get_task_by_group, name='tasks_by_group')
]
