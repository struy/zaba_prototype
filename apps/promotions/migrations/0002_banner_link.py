# Generated by Django 2.2.24 on 2021-08-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='link',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='link'),
        ),
    ]
