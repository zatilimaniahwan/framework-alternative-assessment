# Generated by Django 5.2.3 on 2025-06-24 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AidRequestManagement', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aidrequest',
            name='requester_name',
            field=models.CharField(max_length=255),
        ),
    ]
