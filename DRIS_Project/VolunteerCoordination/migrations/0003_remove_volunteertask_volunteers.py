# Generated by Django 5.2.3 on 2025-06-24 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VolunteerCoordination', '0002_volunteertask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteertask',
            name='volunteers',
        ),
    ]
