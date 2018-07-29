from django.db import models
from adverts.models import Advert, Location
from django_countries.fields import CountryField
from django.urls import reverse



# Create your models here.

class JobType(models.Model):
    name = models.CharField(max_length=42)

    def __str__(self):
        return self.name


class Job(Advert):
    """
    :type
    location
    duration
    payment
    expired
    """
    jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    DURATION = (('ft', 'Fulltime'),
                ('pt', 'Parttime'),)
    duration = models.CharField(
        max_length=2,
        choices=DURATION,
        default='ft'
    )
    countries = CountryField(multiple=True, default='EN')
    salary = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('jobs_cbv:job_edit', kwargs={'pk': self.pk})
