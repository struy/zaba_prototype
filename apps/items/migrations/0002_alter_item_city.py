# Generated by Django 4.0.7 on 2022-10-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='city',
            field=models.CharField(default='Chicago,IL', max_length=50, verbose_name='city'),
        ),
    ]