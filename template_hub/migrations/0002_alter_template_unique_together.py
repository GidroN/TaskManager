# Generated by Django 5.0.3 on 2024-04-03 10:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template_hub', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='template',
            unique_together={('user', 'id')},
        ),
    ]