# Generated by Django 2.2.28 on 2022-11-13 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0002_alter_gift_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gift',
            name='expires',
        ),
    ]
