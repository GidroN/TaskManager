# Generated by Django 5.0.3 on 2024-03-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_exportedjsonhistory_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportedjsonhistory',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]