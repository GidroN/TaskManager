from django.urls import path

from .views import TaskListView, AddTaskView, AddGroupView, UpdateTaskView, DetailTaskView, DeleteTaskView, \
    GroupListView, UpdateGroupView, DeleteGroupView, DownloadFileView, \
    DeleteExportedJSONHistoryView, DisplayAccountInfo, JsonExportView

urlpatterns = [
    path('', TaskListView.as_view(), name='today_tasks'),

    path('settings/', DisplayAccountInfo.as_view(), name='account_info'),

    path('settings/json_export/', JsonExportView.as_view(), name='export_json'),
    path('settings/json_export/dowload_file/<int:file_id>/', DownloadFileView.as_view(), name='download_file'),
    path('settings/json_export/delete_file/<int:file_id>/', DeleteExportedJSONHistoryView.as_view(), name='delete_file'),

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
