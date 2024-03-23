from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm, GroupForm
from .models import Task, Group
from .utils import FixedGroupsCalculator, get_groups_context_data, UserAccessMixin


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'app/task_list.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.calculator = FixedGroupsCalculator()

    def get_queryset(self):
        group_slug = self.kwargs.get('group_slug', None)
        group_slug = 'today' if not group_slug else group_slug
        self.group = Group.objects.get(slug=group_slug, user=self.request.user)
        fixed_groups = self.calculator.get_fixed_groups_data(self.request.user)
        return fixed_groups.get(self.group.slug, Task.objects.filter(group=self.group))

    def get_context_data(self, **kwargs):
        context_data = {'tasks': Task.objects.filter(group=self.group), 'current_group': self.group}
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class DetailTaskView(LoginRequiredMixin, UserAccessMixin, DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context_data = super(DetailTaskView, self).get_context_data(**kwargs)
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class UpdateTaskView(LoginRequiredMixin, UserAccessMixin, UpdateView):
    model = Task
    template_name = 'app/form.html'
    form_class = TaskForm

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def get_context_data(self, **kwargs):
        context_data = super(UpdateTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Изменить задачу'
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class AddTaskView(LoginRequiredMixin, UserAccessMixin, CreateView):
    form_class = TaskForm
    template_name = 'app/form.html'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('tasks_by_group', kwargs={'group_slug': group_slug})

    def form_valid(self, form):
        group_slug = self.kwargs['group_slug']
        group = Group.objects.get(slug=group_slug)
        form.instance.group = group
        form.instance.due_date = timezone.localdate()
        return super(AddTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(AddTaskView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить задачу'
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class DeleteTaskView(LoginRequiredMixin, UserAccessMixin, DeleteView):
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
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'app/group_list.html'

    def get_queryset(self):
        return Group.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super(GroupListView, self).get_context_data(**kwargs)
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class DetailGroupView(LoginRequiredMixin, UserAccessMixin, DetailView):
    model = Group
    template_name = 'app/group_detail.html'
    context_object_name = 'group'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context_data = super(DetailGroupView, self).get_context_data(**kwargs)
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class AddGroupView(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    template_name = 'app/form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context_data = super(AddGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Добавить Группу'
        context_data.update(get_groups_context_data(self.request.user))
        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddGroupView, self).form_valid(form)


class UpdateGroupView(LoginRequiredMixin, UserAccessMixin, UpdateView):
    form_class = GroupForm
    model = Group
    template_name = 'app/form.html'
    success_url = reverse_lazy('group_list')
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context_data = super(UpdateGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Изменить группу'
        context_data.update(get_groups_context_data(self.request.user))
        return context_data


class DeleteGroupView(LoginRequiredMixin, UserAccessMixin, DeleteView):
    model = Group
    template_name = 'app/confirm_delete.html'
    context_object_name = 'item'
    success_url = reverse_lazy('group_list')
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context_data = super(DeleteGroupView, self).get_context_data(**kwargs)
        context_data['action'] = 'Удалить группу'
        context_data['come_from'] = 'group'
        context_data.update(get_groups_context_data(self.request.user))
        return context_data
