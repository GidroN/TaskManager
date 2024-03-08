from django.utils import timezone

from .models import Task, Group


class FixedGroupsCalculator:

    def get_fixed_groups_data(self):
        return {
            'planned': self.get_scheduled_tasks(),
            'overdue': self.get_overdue_tasks(),
            'all-tasks': Task.objects.all(),
            'today': self.get_tasks_for_today(),
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
        fixed_groups = self.get_fixed_groups_data()
        return Group.objects.filter(slug__in=list(fixed_groups.keys()))


def get_groups_context_data():
    calculator = FixedGroupsCalculator()
    fixed_groups = calculator.get_fixed_groups_data()
    groups = Group.objects.exclude(slug__in=list(fixed_groups.keys()))
    return {
        'groups': groups,
        'fixed_groups': calculator.get_fixed_groups(),
    }