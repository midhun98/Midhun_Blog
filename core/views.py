from django.shortcuts import render

# Create your views here.
def BASE(request):
    if request.method == "GET":
        return render(request, 'details.html')