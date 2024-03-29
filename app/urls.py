from django.urls import path
from .views import TaskListView, AddTaskView, AddGroupView, UpdateTaskView, DetailTaskView, DeleteTaskView, \
    GroupListView, UpdateGroupView, DeleteGroupView, display_account_info, export_json, download_file_view, \
    DeleteExportedJSONHistoryView, UpdateUserView

urlpatterns = [
    path('', TaskListView.as_view(), name='today_tasks'),

    path('settings/', display_account_info, name='account_info'),
    path('settings/change_email', UpdateUserView.as_view(), name='change_email',),

    path('settings/json_export', export_json, name='export_json'),
    path('settings/dowload_file/<int:file_id>', download_file_view, name='download_file'),
    path('settings/delete_file/<int:file_id>', DeleteExportedJSONHistoryView.as_view(), name='delete_file'),

    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/add/', AddGroupView.as_view(), name='add_group'),
    path('groups/<slug:group_slug>/edit/', UpdateGroupView.as_view(), name='edit_group'),
    path('groups/<slug:group_slug>/delete/', DeleteGroupView.as_view(), name='delete_group'),

    path('groups/<slug:group_slug>/', TaskListView.as_view(), name='tasks_by_group'),
    path('groups/<slug:group_slug>/add/', AddTaskView.as_view(), name='add_task_to_group'),
    path('groups/<slug:group_slug>/<int:pk>/', DetailTaskView.as_view(), name='detail_task'),
    path('groups/<slug:group_slug>/<int:pk>/edit/', UpdateTaskView.as_view(), name='edit_task'),
    path('groups/<slug:group_slug>/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
]
