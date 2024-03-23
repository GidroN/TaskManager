from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone


from .models import Task, Group


class FixedGroupsCalculator:

    FIXED_GROUPS = ['today', 'planned', 'overdue', 'all-tasks']

    def get_fixed_groups_data(self, user):
        return {
            'today': self.get_tasks_for_today().filter(group__user=user),
            'planned': self.get_scheduled_tasks().filter(group__user=user),
            'overdue': self.get_overdue_tasks().filter(group__user=user),
            'all-tasks': Task.objects.filter(group__user=user),
        }

    @staticmethod
    def get_tasks_for_today():
        now = timezone.now()
        return Task.objects.filter(due_date=now.date()).exclude(due_time__lt=now.time())

    @staticmethod
    def get_scheduled_tasks():
        now = timezone.now()
        return Task.objects.filter(due_date__gt=now.date()) | \
            Task.objects.filter(due_date=now.date(), due_time__gt=now.time())

    @staticmethod
    def get_overdue_tasks():
        now = timezone.now()
        return Task.objects.filter(due_date__lt=now.date()) | \
            Task.objects.filter(due_date=now.date(), due_time__lt=now.time())

    def get_fixed_groups(self):
        return Group.objects.filter(slug__in=self.FIXED_GROUPS)


def get_groups_context_data(user):
    calculator = FixedGroupsCalculator()
    groups = Group.objects.exclude(slug__in=calculator.FIXED_GROUPS).filter(user=user)
    return {
        'groups': groups,
        'fixed_groups': calculator.get_fixed_groups().filter(user=user),
    }


class UserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        group_slug = self.kwargs.get('group_slug')
        task_id = self.kwargs.get('pk')

        group = get_object_or_404(Group, slug=group_slug, user=user)

        if task_id:
            get_object_or_404(Task, id=task_id, group=group)

        return super().dispatch(request, *args, **kwargs)
