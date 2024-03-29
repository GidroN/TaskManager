import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm, GroupForm, ExportJSONForm
from .models import Task, Group
from .utils import FixedGroupsCalculator, JsonExport, JsonImport
from .mixins import GroupsDataMixin, UserAccessMixin


@login_required
def display_account_info(request, user):
    if str(request.user) == str(user):
        return render(request, 'app/account_page.html', {'user': user})
    else:
        return redirect('today_tasks', permanent=True)


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
        context_data['action'] = 'Добавить задачу'
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


@login_required
def export_json(request, user):
    if request.method == 'POST':
        form = ExportJSONForm(request.POST, user=request.user)
        if form.is_valid():
            groups = form.cleaned_data['groups']

            data = JsonExport(groups).extract_data()
            response = HttpResponse(json.dumps(data), content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'

            return response
    else:
        form = ExportJSONForm(user=request.user)

    return render(request, 'app/json_export.html', {'form': form})
