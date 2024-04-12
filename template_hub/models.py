import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    downloads = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='template_hub/template_storage')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-downloads']
        unique_together = ('user', 'id')
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']
        unique_together = ('template', 'id')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
