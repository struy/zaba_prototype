import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Advert(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['updated_at']

    def __unicode__(self):
        return self.title

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title


class Location(models.Model):
    city = models.CharField(max_length=42, default='Chicago')
    neighborhoods = models.CharField(max_length=42, blank=True)
    # zipcode = models.IntegerField()

    class Meta:
        ordering = ['city']

    def __unicode__(self):
        return self.city

    def __str__(self):
        return self.city
