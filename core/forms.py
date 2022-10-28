from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from . import models
from django.contrib.auth.models import User
import re


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        email = cleaned_data.get('email')
        content = cleaned_data.get('content')
        subject = cleaned_data.get('subject')

        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', "Enter a valid email address.")

        if content in [None, '']:
            self.add_error('content', "Enter a content.")

        if subject in [None, '']:
            self.add_error('subject', "Enter a name.")




class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'User Name',
            'password': 'Password',
            'confirm_password': 'Confirm password',
        }

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        if User.objects.filter(email=email):
            self.add_error('email', "This email already registered.")

        if User.objects.filter(username=username):
            self.add_error('username', "This username is already registered.")

        if password != confirm_password:
            self.add_error("confirm_password", "passwords do not match.")


class ProfileCreateForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=models.Role.objects.all(), label='Role', required=True)

    class Meta:
        model = models.Profile
        fields = ('role', 'country', 'mobile')
        labels = {
            'role': 'Role',
            'country': 'Country',
            'mobile': 'Mobile',
        }

    def clean(self):
        cleaned_data = super(ProfileCreateForm, self).clean()
        mobile = cleaned_data.get('mobile')
        regnum = r'^([0-9]{10})$'
        try:
            obj2 = re.match(regnum, mobile)
            if obj2:
                pass
            else:
                self.add_error('mobile', "Please enter valid number")
        except:
            self.add_error('mobile', "Please enter valid number")

    def __init__(self, user, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
