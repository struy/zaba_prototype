from django import forms

from .models import Banner
from django_svg_image_form_field import SvgAndImageFormField


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        exclude = []
        field_classes = {
            'image': SvgAndImageFormField,
        }