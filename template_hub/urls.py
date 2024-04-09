from django.urls import path

from .views import TemplateListView, TemplateDetailView, TemplateCreateView, TemplateUpdateView, TemplateDeleteView, \
    JsonImportView, TemplateManagement

urlpatterns = [
    path('', TemplateListView.as_view(), name='template-list'),

    path('template/my/', TemplateManagement.as_view(), name='template-management'),

    path('template/add/', TemplateCreateView.as_view(), name='template-create'),
    path('template/<int:template_id>/', TemplateDetailView.as_view(), name='template-detail'),
    path('template/<int:template_id>/edit/', TemplateUpdateView.as_view(), name='template-update'),
    path('template/<int:template_id>/delete/', TemplateDeleteView.as_view(), name='template-delete'),
    path('template/download/<int:template_id>/', JsonImportView.as_view(), name='template-download'),
]