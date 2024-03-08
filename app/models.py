from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from slugify import slugify


class Task(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    due_date = models.DateField(blank=True, default=timezone.localdate)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='tasks')
    date_complete = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_groups')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        unique_together = ('user', 'name')
