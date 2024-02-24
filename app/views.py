from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import *


# def index(request):
#     reverse_path = reverse('today_tasks')
#     return redirect(reverse_path, permanent=True)


def get_task_by_group(request, group_id):
    tasks = Task.objects.filter(group__id=group_id)
    groups = Group.objects.all()
    group_name = Group.objects.filter(id=group_id).first().name
    return render(request, 'app/task_list.html', {'groups': groups, 'tasks': tasks, 'group_name': group_name})


def get_today_tasks(request):
    groups = Group.objects.all()
    today = timezone.now().today()
    tasks = Task.objects.filter(due_date__date=today)
    return render(request, 'app/task_list.html', {'groups': groups, 'tasks': tasks, 'group_name': 'Задачи на сегодня'})