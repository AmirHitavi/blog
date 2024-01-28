from django import forms
from .models import Subscribe
from django.utils.translation import gettext_lazy as _


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        labels = {'email': _("")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = 'Enter your email'
