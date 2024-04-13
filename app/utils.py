import os

from django.contrib.auth.models import User
from django.db import models, transaction
from django.http import HttpResponse
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


class JsonExport:
    def __init__(self, groups: models.QuerySet[Group]):
        self._groups = groups

    @staticmethod
    def convert_tasks_to_list(tasks: models.QuerySet[Task]) -> list[dict]:
        data = [{'name': task.name, 'description': task.description} for task in tasks]
        return data

    def extract_data(self) -> dict:
        data = {}
        for group in self._groups:
            data[group.name] = self.convert_tasks_to_list(Task.objects.filter(group=group))

        return data


class JsonImport:
    def __init__(self, data: dict, user: User):
        self.data = data
        self.user = user

    def import_data(self):
        with transaction.atomic():
            for group, tasks in self.data.items():
                try:
                    group = Group.objects.get(name=group, user=self.user)
                except Group.DoesNotExist:
                    group = Group.objects.create(name=group, user=self.user)

                for task in tasks:
                    try:
                        Task.objects.get(group=group, name=task['name'], description=task['description'])
                    except Task.DoesNotExist:
                        Task.objects.create(group=group, name=task['name'], description=task['description'])


def download_file(file):
    file_path = file.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("Извините, файл не найден.", status=404)
