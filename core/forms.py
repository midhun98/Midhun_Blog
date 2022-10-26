from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


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
