# Generated by Django 5.0.3 on 2024-04-12 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template_hub', '0005_alter_comment_created_alter_comment_template_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('template', 'id')},
        ),
    ]
