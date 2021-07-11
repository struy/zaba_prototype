from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    """ file will be uploaded to MEDIA_ROOT /<class_name>/<year>/<month>/<day>/user_<id>_<filename>"""
    return f'{instance.__class__.__name__.lower()}s/{instance.local}/{instance.size}/{filename}'


class Promote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name=_('author'))
    name = models.CharField(max_length=200, verbose_name=_('name'))
    paid = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Area(models.Model):
    AREAS = (('h', _('Header')),
             ('rs', _('Right Sidebar')),
             ('ls', _('Left Sidebar')),
             )
    area = models.CharField(max_length=2, choices=AREAS)

    class Meta:
        ordering = ('area',)

    def __str__(self):
        d_areas = dict(self.AREAS)
        return str(d_areas[self.area])


class Banner(models.Model):
    LOCALES = (('en', 'English'),
               ('uk', 'Ukraine'),
               ('ru', 'Russian'),
               ('pl', 'Polish'),
               )

    SIZES = (
        ("xs", _("Extra small")),
        ("sm", _("Small")),
        ("md", _("Medium")),
        ("lg", _("Large")),
        ("xl", _("Extra large")),
    )

    size = models.CharField(max_length=2, choices=SIZES)
    local = models.CharField(max_length=2, choices=LOCALES, default='en')
    image = models.ImageField(upload_to=user_directory_path)
    promote = models.ForeignKey(Promote, on_delete=models.CASCADE, related_name='banners')
    areas = models.ManyToManyField(Area)

    def __str__(self):
        return ""
