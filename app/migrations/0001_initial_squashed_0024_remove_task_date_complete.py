# Generated by Django 5.0.3 on 2024-04-13 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [('app', '0001_initial'), ('app', '0002_remove_group_tasks_task_group'), ('app', '0003_group_user'),
                ('app', '0004_task_due_time_alter_task_due_date'), ('app', '0005_alter_task_due_date'),
                ('app', '0006_alter_task_name'), ('app', '0007_alter_group_name_alter_task_name'),
                ('app', '0008_group_slug'), ('app', '0009_alter_group_slug'),
                ('app', '0010_alter_group_name_alter_group_unique_together'), ('app', '0011_alter_group_user'),
                ('app', '0012_add_default_group_data'), ('app', '0013_remove_group_description'),
                ('app', '0014_alter_task_options'), ('app', '0015_alter_task_options'),
                ('app', '0016_alter_task_due_date'), ('app', '0017_exportedjsonhistory'),
                ('app', '0018_remove_exportedjsonhistory_datetime'),
                ('app', '0019_exportedjsonhistory_datetime_and_more'),
                ('app', '0020_alter_exportedjsonhistory_datetime'),
                ('app', '0021_exportedjsonhistory_user_alter_group_user'),
                ('app', '0022_alter_exportedjsonhistory_user'), ('app', '0023_alter_exportedjsonhistory_options'),
                ('app', '0024_remove_task_date_complete')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_groups',
                                           to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ExportedJsonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=55)),
                ('file', models.FileField(upload_to='app/json_file_storage')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'История выгрузки json',
                'verbose_name_plural': 'История выгрузки json',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True)),
                ('group',
                 models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks',
                                   to='app.group')),
                ('due_time', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-is_active'],
            },
        ),
    ]
