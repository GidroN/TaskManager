# Generated by Django 5.0.3 on 2024-03-29 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_exportedjsonhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exportedjsonhistory',
            name='datetime',
        ),
    ]
