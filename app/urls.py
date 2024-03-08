from django.urls import path
from .views import TaskListView, AddTaskView, AddGroupView, UpdateTaskView, DetailTaskView, DeleteTaskView

urlpatterns = [
    path('', TaskListView.as_view(), name='today_tasks'),
    path('groups/add', AddGroupView.as_view(), name='add_group'),
    path('groups/<slug:group_slug>', TaskListView.as_view(), name='tasks_by_group'),
    path('groups/<slug:group_slug>/add', AddTaskView.as_view(), name='add_task_to_group'),
    path('groups/<slug:group_slug>/<int:pk>', DetailTaskView.as_view(), name='detail_task'),
    path('groups/<slug:group_slug>/<int:pk>/edit', UpdateTaskView.as_view(), name='edit_task'),
    path('groups/<slug:group_slug>/<int:pk>/delete', DeleteTaskView.as_view(), name='delete_task'),
]
