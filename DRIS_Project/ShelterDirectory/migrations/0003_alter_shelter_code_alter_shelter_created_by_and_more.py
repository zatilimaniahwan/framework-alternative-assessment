# Generated by Django 5.2.3 on 2025-06-23 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShelterDirectory', '0002_initial'),
        ('UserManagement', '0002_alter_role_id_alter_role_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelter',
            name='code',
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='shelter',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shelters_created', to='UserManagement.authority'),
        ),
        migrations.AlterField(
            model_name='shelter',
            name='location',
            field=models.TextField(max_length=255),
        ),
    ]
