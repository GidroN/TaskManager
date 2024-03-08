from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.utils import timezone

from .forms import TaskForm, GroupForm
from .models import Task, Group
from .utils import FixedGroupsCalculator, get_groups_context_data


class TaskListView(ListView):
    template_name = 'app/task_list.html'
    context_object_name = 'tasks'

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.group = None
        self.calculator = FixedGroupsCalculator()
        self.fixed_groups = self.calculator.get_fixed_groups_data()

    def get_queryset(self):
        group_slug = self.kwargs.get('group_slug', None)
        group_slug = 'today' if not group_slug else group_slug
        self.group = get_object_or_404(Group, slug=group_slug)
        return self.fixed_groups.get(self.group.slug, Task.objects.filter(group=self.group))

    def get_context_data(self, **kwargs):
        context_data = super(TaskListView, self).get_context_data(**kwargs)
        context_data['current_group'] = self.group
        context_data.update(get_groups_context_data())
        return context_data


class DetailTaskView(DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context_data = super(DetailTaskView, self).get_context_data(**kwargs)
        context_data.update(get_groups_context_data())
        return context_data


class UpdateTaskView(UpdateView):
    model = Task
    template_name = 'app/form.html'
    form_class = TaskForm

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def get_context_data(self, **kwargs):
        context_data = super(UpdateTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Изменить задачу'
        context_data.update(get_groups_context_data())
        return context_data


class AddTaskView(CreateView):
    form_class = TaskForm
    template_name = 'app/form.html'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def form_valid(self, form):
        group_slug = self.kwargs['group_slug']
        group = Group.objects.get(slug=group_slug)
        form.instance.group = group
        return super(AddTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(AddTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить задачу'
        context_data.update(get_groups_context_data())
        return context_data


class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'app/task_confirm_delete.html'
    context_object_name = 'task'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def get_context_data(self, **kwargs):
        context_data = super(DeleteTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить задачу'
        context_data.update(get_groups_context_data())
        return context_data


class AddGroupView(CreateView):
    form_class = GroupForm
    template_name = 'app/form.html'
    success_url = reverse_lazy('today_tasks')

    def get_context_data(self, **kwargs):
        context_data = super(AddGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить Группу'
        context_data.update(get_groups_context_data())
        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddGroupView, self).form_valid(form)

