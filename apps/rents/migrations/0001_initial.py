# Generated by Django 2.2.17 on 2020-11-29 03:03

import apps.adverts.models
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('name_en', models.CharField(max_length=42, null=True)),
                ('name_ru', models.CharField(max_length=42, null=True)),
                ('name_pl', models.CharField(max_length=42, null=True)),
                ('name_uk', models.CharField(max_length=42, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', verbose_name='slug')),
                ('expires', models.DateField(blank=True, help_text='Format mm/dd/yyyy', null=True, validators=[
                    apps.adverts.models.validate_expires], verbose_name='expires')),
                ('local', models.CharField(choices=[('en', 'en_US'), ('uk', 'uk_UA'), ('ru', 'ru_RU'), ('pl', 'pl_PL')], default='en', max_length=2)),
                ('city', models.CharField(default='Chicago', max_length=50, verbose_name='city')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='map')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.adverts.models.user_directory_path)),
                ('bathrooms', models.PositiveSmallIntegerField(default=1)),
                ('bedrooms', models.PositiveSmallIntegerField(default=1)),
                ('price', models.PositiveIntegerField()),
                ('pet_policy', models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'Dogs'), (2, 'Cats'), (3, 'Dogs and Cats'), (4, 'Any')], default=0)),
                ('furnished', models.BooleanField()),
                ('prefer_sex', models.CharField(choices=[('a', 'any'), ('w', 'woman'), ('m', 'man')], default='a', max_length=1)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('favourites', models.ManyToManyField(blank=True, default=None, related_name='favourite_rents', to=settings.AUTH_USER_MODEL)),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rents.PropertyType', verbose_name='property type')),
            ],
            options={
                'ordering': ['modified'],
                'abstract': False,
            },
        ),
    ]
