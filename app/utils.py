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
        return Task.objects.filter(due_date=now.date())

    @staticmethod
    def get_scheduled_tasks():
        now = timezone.now()
        return Task.objects.filter(due_date__gt=now.date())

    @staticmethod
    def get_overdue_tasks():
        now = timezone.now()
        return Task.objects.filter(due_date__lt=now.date())

    def get_fixed_groups(self):
        return Group.objects.filter(slug__in=self.FIXED_GROUPS)


def get_groups_context_data(user):
    calculator = FixedGroupsCalculator()
    groups = Group.objects.exclude(slug__in=calculator.FIXED_GROUPS).filter(user=user)
    return {
        'groups': groups,
        'fixed_groups': calculator.get_fixed_groups().filter(user=user),
    }
