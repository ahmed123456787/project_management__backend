# Generated by Django 5.1.2 on 2024-11-01 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_project_task_remove_task_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_list',
            new_name='sprint',
        ),
    ]