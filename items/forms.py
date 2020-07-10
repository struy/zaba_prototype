from django import forms
from django.contrib.gis import forms as gis_forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from zaba.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from django.utils.translation import get_language
from django_select2 import forms as s2forms
from .models import Item


class CityWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "city__icontains",
    ]


class ItemForm(forms.ModelForm):
    expires = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )
    # captcha = ReCaptchaField(
    #     public_key=RECAPTCHA_PUBLIC_KEY,
    #     private_key=RECAPTCHA_PRIVATE_KEY,
    #     widget=ReCaptchaV3,
    # )

    class Meta:
        model = Item
        fields = ['condition', 'title', 'description', 'price', 'image', 'expires', 'city', 'address', 'point']
        widgets = {
            'point': gis_forms.OSMWidget(attrs={
                'default_lon': -88,
                'default_lat': 41.9,
                'map_width': 800,
                'map_height': 500,
                'default_zoom': 10,
                'city': CityWidget
            }),
            # 'captcha': ReCaptchaV3(
            #     api_params={'hl': get_language()[:2], 'badge': 'inline', }
            # ),
        }
