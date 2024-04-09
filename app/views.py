import json

from django.core.files.base import ContentFile
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm, GroupForm, ExportJsonForm
from .models import Task, Group, ExportedJsonHistory
from .utils import FixedGroupsCalculator, JsonExport, download_file
from .mixins import GroupsDataMixin, UserAccessMixin


class DisplayAccountInfo(LoginRequiredMixin, TemplateView):
    template_name = 'app/account_page.html'


class DownloadFileView(LoginRequiredMixin, View):
    def get(self, request, file_id):
        file = get_object_or_404(ExportedJsonHistory, id=file_id).file
        return download_file(file)


class JsonExportView(LoginRequiredMixin, FormView):
    template_name = 'app/json_export.html'
    form_class = ExportJsonForm
    success_url = reverse_lazy('export_json')

    def form_valid(self, form):
        groups = form.cleaned_data['groups']
        data = JsonExport(groups).extract_data()

        json_data = json.dumps(data)
        json_file_name = f'{self.request.user.username}_export_{timezone.now().strftime("%Y-%m-%d_%H:%M:%S")}.json'

        exported_json = ExportedJsonHistory(user=self.request.user)
        exported_json.file.save(json_file_name, ContentFile(json_data))

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(JsonExportView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super(JsonExportView, self).get_context_data(**kwargs)
        context_data['objects'] = ExportedJsonHistory.objects.filter(user=self.request.user)
        return context_data


class DeleteExportedJSONHistoryView(LoginRequiredMixin, View):
    def get(self, request, file_id):
        try:
            file_to_delete = ExportedJsonHistory.objects.get(user=request.user, id=file_id)
            file_to_delete.delete()
            return redirect('export_json')
        except ExportedJsonHistory.DoesNotExist:
            return redirect('today_tasks')


class TaskListView(LoginRequiredMixin, GroupsDataMixin, ListView):
    template_name = 'app/task_list.html'
    context_object_name = 'tasks'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.calculator = FixedGroupsCalculator()

    def get_queryset(self):
        group_slug = self.kwargs.get('group_slug')
        group_slug = 'today' if not group_slug else group_slug
        self.group = Group.objects.get(slug=group_slug, user=self.request.user)
        fixed_groups = self.calculator.get_fixed_groups_data(self.request.user)
        return fixed_groups.get(self.group.slug, Task.objects.filter(group=self.group))

    def get_context_data(self, **kwargs):
        context_data = super(TaskListView, self).get_context_data(**kwargs)
        context_data['current_group'] = self.group
        return context_data


class DetailTaskView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'


class UpdateTaskView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, UpdateView):
    model = Task
    template_name = 'app/form.html'
    form_class = TaskForm

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def get_context_data(self, **kwargs):
        context_data = super(UpdateTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Изменить задачу'
        return context_data


class AddTaskView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, CreateView):
    form_class = TaskForm
    template_name = 'app/form.html'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def form_valid(self, form):
        group_slug = self.kwargs['group_slug']
        group = Group.objects.get(slug=group_slug, user=self.request.user)
        form.instance.group = group
        form.instance.due_date = timezone.localdate()
        return super(AddTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(AddTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить задачу'
        return context_data


class DeleteTaskView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, DeleteView):
    model = Task
    template_name = 'app/confirm_delete.html'
    context_object_name = 'item'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def get_context_data(self, **kwargs):
        context_data = super(DeleteTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Удалить задачу'
        context_data['come_from'] = 'task'
        return context_data


class GroupListView(LoginRequiredMixin, GroupsDataMixin, ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'app/group_list.html'

    def get_queryset(self):
        return Group.objects.filter(user=self.request.user)


class AddGroupView(LoginRequiredMixin, GroupsDataMixin, CreateView):
    form_class = GroupForm
    template_name = 'app/form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context_data = super(AddGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить Группу'
        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddGroupView, self).form_valid(form)


class UpdateGroupView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, UpdateView):
    form_class = GroupForm
    model = Group
    template_name = 'app/form.html'
    success_url = reverse_lazy('group_list')
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context_data = super(UpdateGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Изменить группу'
        return context_data


class DeleteGroupView(LoginRequiredMixin, UserAccessMixin, GroupsDataMixin, DeleteView):
    model = Group
    template_name = 'app/confirm_delete.html'
    context_object_name = 'item'
    success_url = reverse_lazy('group_list')
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Удалить группу'
        context['tasks_count'] = Task.objects.filter(group=self.object).count()
        return context
