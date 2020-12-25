from django import forms
from django.contrib.auth.models import User
from zaba.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from django.utils.translation import get_language
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    captcha = ReCaptchaField(
        public_key=RECAPTCHA_PUBLIC_KEY,
        private_key=RECAPTCHA_PRIVATE_KEY,
        widget=ReCaptchaV3,
        label='',
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'captcha': ReCaptchaV3(
                api_params={'hl': get_language()[:2], 'badge': 'inline', }
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ContactUserForm(forms.Form):
    from_email = forms.EmailField(required=True, label=_('From  email'))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_('Message'))
