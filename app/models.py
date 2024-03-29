import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from slugify import slugify


class Task(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    due_date = models.DateField(blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='tasks')
    date_complete = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.localdate()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_active']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_groups', null=True, blank=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def count_tasks(self):
        return Task.objects.filter(group__name=self.name, group__user=self.user).count()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        unique_together = ('user', 'name')


class ExportedJsonHistory(models.Model):
    name = models.CharField(max_length=55, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='app/json_file_storage')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = timezone.now().strftime('%d %B %Y %H:%M')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'История выгрузки json'
        verbose_name_plural = verbose_name
