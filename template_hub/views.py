import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView, TemplateView

from app.utils import JsonImport

from .forms import TemplateForm
from .mixins import UserAccessMixin
from .models import Template, Comment


class JsonImportView(LoginRequiredMixin, View):
    def get(self, request, template_id):
        template = Template.objects.get(id=template_id)
        file_path = template.file.path

        with open(file_path, 'r') as file:
            data = json.load(file)

        JsonImport(data, self.request.user).import_data()

        template.downloads += 1
        template.save()

        return redirect('today_tasks')


class CommentAddView(LoginRequiredMixin, View):
    def post(self, request, template_id):
        text = request.POST.get('comment')
        if text:
            template = Template.objects.get(id=template_id)
            Comment.objects.create(user=request.user, template=template, text=text)
        return redirect('template-detail',  template_id=template_id)


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, template_id, comment_id):
        template = Template.objects.get(id=template_id)
        Comment.objects.get(template=template, id=comment_id).delete()
        return redirect('template-detail', template_id=template_id)


class TemplateManagement(LoginRequiredMixin, ListView):
    template_name = 'template_hub/template_management.html'
    model = Template
    context_object_name = 'templates'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search-query')

        if not search_query:
            return queryset

        return queryset.filter(name__icontains=search_query)


class TemplateListView(LoginRequiredMixin, ListView):
    template_name = 'template_hub/template_list.html'
    model = Template
    context_object_name = 'templates'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search-query')
        filter_by = self.request.GET.get('filter-by') or 'name'
        order_by = self.request.GET.get('order-by') or 'asc'

        if not search_query:
            return queryset

        if filter_by == 'name':
            queryset = queryset.filter(name__icontains=search_query)
        elif filter_by == 'user__username':
            queryset = queryset.filter(user__username__icontains=search_query)

        if order_by == 'desc':
            queryset = queryset.order_by(f'-{filter_by}')
        else:
            queryset = queryset.order_by(f'{filter_by}')

        return queryset


class TemplateDetailView(LoginRequiredMixin, DetailView):
    template_name = 'template_hub/template_detail.html'
    model = Template
    context_object_name = 'template'
    pk_url_kwarg = 'template_id'


class TemplateCreateView(LoginRequiredMixin, CreateView):
    template_name = 'template_hub/form.html'
    model = Template
    form_class = TemplateForm
    success_url = reverse_lazy('template-management')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['action'] = 'Добавить шаблон'
        return context_data


class TemplateUpdateView(LoginRequiredMixin, UserAccessMixin, UpdateView):
    template_name = 'template_hub/form.html'
    model = Template
    form_class = TemplateForm
    pk_url_kwarg = 'template_id'
    success_url = reverse_lazy('template-management')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['action'] = 'Изменить шаблон'
        return context_data


class TemplateDeleteView(LoginRequiredMixin, UserAccessMixin, DeleteView):
    template_name = 'template_hub/confirm_delete.html'
    model = Template
    context_object_name = 'template'
    pk_url_kwarg = 'template_id'
    success_url = reverse_lazy('template-management')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['action'] = 'Удалить шаблон'
        return context_data
