from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=50)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        content = cleaned_data.get('content')
        subject = cleaned_data.get('subject')

        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', "Enter a valid email address.")

        if name in [None, '']:
            self.add_error('name', "Enter a name.")

        if content in [None, '']:
            self.add_error('content', "Enter a content.")

        if subject in [None, '']:
            self.add_error('subject', "Enter a name.")
