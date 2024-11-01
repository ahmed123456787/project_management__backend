# Generated by Django 5.1.2 on 2024-10-25 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='task',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='core.task'),
        ),
    ]
