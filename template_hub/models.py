import os

from django.db import models
from django.contrib.auth.models import User


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    downloads = models.IntegerField(default=0)
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
