import datetime


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify



class Advert(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['updated_at']
        abstract = True

    def __unicode__(self):
        return self.title

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        words = '-'.join(self.title.split()[:4])
        text = slugify(words, allow_unicode=True)
        count = Advert.objects.filter(slug__startswith=text).count()
        if count != 0:
            text = '%s-%d' % (text, count)
        self.slug = text
        return super(Advert, self).save(*args, **kwargs)


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
