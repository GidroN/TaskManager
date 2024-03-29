import json
import os

from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone

from .models import Task, Group, ExportedJsonHistory


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


class JsonExport:
    def __init__(self, groups: QuerySet[Group]):
        self._groups = groups

    @staticmethod
    def convert_tasks_to_dict( tasks: QuerySet[Task]) -> dict:
        data = {}
        for task in tasks:
            data[task.id] = {
                'name': task.name,
                'description': task.description,
            }

        return data

    def extract_data(self) -> dict:
        data = {}
        for group in self._groups:
            data[group.name] = self.convert_tasks_to_dict(Task.objects.filter(group=group))

        return data


class JsonImport:
    def __init__(self):
        ...


def download_file(file_id):
    file_entry = ExportedJsonHistory.objects.get(id=file_id)
    file_path = file_entry.file.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("Извините, файл не найден.", status=404)