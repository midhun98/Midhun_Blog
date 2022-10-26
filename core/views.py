from django.shortcuts import render, redirect
from django.views import generic
from rest_framework.views import APIView
import requests
from . import forms
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

class ProfilePage(APIView):
    def get(self, request):
        if request.method == "GET":
            context = {}
            r = requests.get('https://gh-pinned-repos.egoist.dev/?username=midhun98')
            r_status = r.status_code
            if r_status == 200:
                data = r.json()
                context['pinned_repo'] = data
            return render(request, 'details.html', context)

class ResumePage(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            context = {}
            return render(request, 'resume.html', context)


class ContactsPage(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            context = {}
            form = forms.ContactForm()
            context['communication_form'] = form
            return render(request, 'contacts.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            context = {}
            form = forms.ContactForm(request.POST)
            if form.is_valid():
                name = form.data['name']
                email = form.data['email']
                subject = form.data['subject']
                content = form.data['content']
                print(name)
                print(email)
                print(subject)
                print(content)
                send_mail(subject, subject, email, ['midhunskani@gmail.com'])
                return redirect('contacts_page')
            else:
                messages.warning(request, 'Please enter valid details.')
                form = forms.ContactForm()
                context['communication_form'] = form

            return render(request, 'contacts.html', context)
