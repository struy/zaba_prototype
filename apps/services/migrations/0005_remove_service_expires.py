# Generated by Django 2.2.28 on 2022-11-13 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_service_service_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='expires',
        ),
    ]
