import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView, TemplateView

from app.utils import JsonImport

from .forms import TemplateForm
from .models import Template


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


class TemplateManagement(LoginRequiredMixin, ListView):
    template_name = 'template_hub/template_management.html'
    model = Template
    context_object_name = 'templates'

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)


class TemplateListView(LoginRequiredMixin, ListView):
    template_name = 'template_hub/template_list.html'
    model = Template
    context_object_name = 'templates'


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


class TemplateUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'template_hub/form.html'
    model = Template
    form_class = TemplateForm
    pk_url_kwarg = 'template_id'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['action'] = 'Изменить шаблон'
        return context_data


class TemplateDeleteView(LoginRequiredMixin, DeleteView):
    template_name = ''
    model = Template

