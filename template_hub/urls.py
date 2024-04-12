from django.urls import path

from .views import TemplateListView, TemplateDetailView, TemplateCreateView, TemplateUpdateView, TemplateDeleteView, \
    JsonImportView, TemplateManagement, CommentAddView, CommentDeleteView

urlpatterns = [
    path('', TemplateListView.as_view(), name='template-list'),

    path('my/', TemplateManagement.as_view(), name='template-management'),

    path('add/', TemplateCreateView.as_view(), name='template-create'),
    path('template/<int:template_id>/', TemplateDetailView.as_view(), name='template-detail'),
    path('template/<int:template_id>/edit/', TemplateUpdateView.as_view(), name='template-update'),
    path('template/<int:template_id>/delete/', TemplateDeleteView.as_view(), name='template-delete'),

    path('template/<int:template_id>/add_comment/', CommentAddView.as_view(), name='comment-add'),
    path('template/<int:template_id>/delete_comment/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('template/download/<int:template_id>/', JsonImportView.as_view(), name='template-download'),
]