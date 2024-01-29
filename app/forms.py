from django import forms
from .models import Subscribe, Comment
from django.utils.translation import gettext_lazy as _


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        labels = {'email': _("")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = 'Enter your email'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {"name", "email", "content", "website"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["content"].widget.attrs["placeholder"] = "Type your comment..."
        self.fields["website"].widget.attrs["placeholder"] = "Website"

