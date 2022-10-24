from django.shortcuts import render
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