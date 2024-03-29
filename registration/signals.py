from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from app.models import Group


@receiver(post_save, sender=User)
def add_user_to_default_groups(sender, instance, created, **kwargs):
    if created:
        default_groups = {
            'planned': 'Запланированные задачи',
            'today': 'Задачи на сегодня',
            'overdue': 'Просроченные задачи',
            'all-tasks': 'Все задачи',
        }

        for slug, name in default_groups.items():
            Group.objects.create(slug=slug, name=name, user=instance)
