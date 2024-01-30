from django import forms
from .models import Subscribe, Comment
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = {"username", "email", "password1", "password2"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Enter Username"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat Password"

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        users = User.objects.filter(username=username)

        if users.count():
            raise forms.ValidationError("User already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        users = User.objects.filter(email=email)

        if users.count():
            raise forms.ValidationError("Email already exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2
