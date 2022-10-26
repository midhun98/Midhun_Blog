from django.shortcuts import render
from django.views import generic
from rest_framework.views import APIView
import requests
# Create your views here.

class ProfilePage(APIView):
    def get(self, request):
        if request.method == "GET":
            context = {}
            r = requests.get('https://gh-pinned-repos.egoist.dev/?username=midhun98')
            r_status = r.status_code
            if r_status == 200:
                data = r.json()
                context['pinned_repo']= data
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
            return render(request, 'contacts.html', context)
