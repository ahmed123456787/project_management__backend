# Generated by Django 5.1.3 on 2024-11-18 15:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_sprint_name_alter_task_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('name', 'user')},
        ),
    ]
