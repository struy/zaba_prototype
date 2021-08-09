from django import forms
from django_svg_image_form_field import SvgAndImageFormField

from .models import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        exclude = []
        field_classes = {
            'image': SvgAndImageFormField,
        }
