import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework.views import APIView
import requests
from . import forms, models
from django.core.mail import send_mail
from django.contrib import messages
from django import http
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse


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
                email = form.data['email']
                subject = form.data['subject']
                content = form.data['content']
                send_mail(subject, content, email, ['midhunskani@gmail.com'])
                return redirect('contacts_page')
            else:
                messages.warning(request, 'Please enter valid details.')
                form = forms.ContactForm()
                context['communication_form'] = form

            return render(request, 'contacts.html', context)


class BlogPage(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        form = forms.BlogForm()
        context['blog_form'] = form
        return render(request, 'blog/blog_create.html', context)

    def post(self, request, *args, **kwargs):
        form = forms.BlogForm(request.POST)
        context = {}
        if form.is_valid():
            title = form.data['title']
            content = form.data['content']
            tags = form.data['tags']
            user = request.user
            models.BlogModel.objects.create(user=user, title=title, content=content, tags=tags)
            return redirect('blog_list')
        else:
            messages.warning(request, 'Please enter valid details.')
            form = forms.BlogForm()
            context['blog_form'] = form

        return render(request, 'contacts.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.exists():
                    group = user.groups.all()[0].name
                    if group == "staff":
                        return http.HttpResponseRedirect(reverse('staff_view'))
                    elif group == "admin":
                        return http.HttpResponseRedirect(reverse('admin_view'))
                    elif group == "student":
                        return http.HttpResponseRedirect(reverse('student_view'))
                    elif group == "editor":
                        return http.HttpResponseRedirect(reverse('editor_view'))
                    else:
                        pass
                else:
                    return http.HttpResponseRedirect(reverse('base'))
        else:
            messages.warning(request, 'Username is not valid. Please enter a valid username and password.')
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


class UserCreateView(generic.TemplateView):
    template_name = "user_create.html"

    def get_context_data(self, **kwargs):
        context = {}
        form = forms.UserCreateForm()
        sub_form = forms.ProfileCreateForm(self.request.user)
        context['form'] = form
        context['sub_form'] = sub_form
        return context

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)
        sub_form = forms.ProfileCreateForm(request.user, request.POST)
        if form.is_valid() and sub_form.is_valid():
            password = request.POST.get('password')
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            country = request.POST.get('country')
            mobile = request.POST.get('mobile')
            role = request.POST.get('role')

            roleobj = models.Role.objects.get(id=role)

            user = User(username=username, first_name=first_name, last_name=last_name, email=email, is_staff=True)
            user.set_password(password)
            user.save()
            user.groups.add(roleobj.group)
            userid = user.id
            profile = models.Profile(country=country, mobile=mobile, role_id=roleobj.id, user_id=userid)
            profile.save()
            return http.HttpResponseRedirect(reverse('login'))
        else:
            return render(request, self.template_name, {'form': form, 'sub_form': sub_form})


class BlogListView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        data = models.BlogModel.objects.values('title', 'tags', 'content', 'id')
        context['data'] = data
        return render(request, 'blog/blog_list.html', context)


class BlogDetailView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        profile = models.BlogModel.objects.get(id=self.kwargs['pk'])
        context['profile'] = profile
        return render(request, 'blog/blog_detail.html', context)


class BlogUpdateView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        blog = models.BlogModel.objects.get(id=self.kwargs['pk'])
        blog_data = {'content': blog.content, 'tags': blog.tags, 'title': blog.title}
        form = forms.BlogForm(initial=blog_data)
        context['blog_form'] = form
        return render(request, 'blog/blog_update.html', context)

    def post(self, request, *args, **kwargs):
        form = forms.BlogForm(request.POST)
        context = {}
        if form.is_valid():
            title = form.data['title']
            content = form.data['content']
            tags = form.data['tags']
            models.BlogModel.objects.filter(id=self.kwargs['pk']).update(title=title, content=content, tags=tags,
                                                                         updated_at=datetime.datetime.now())
            return redirect('blog_list')
        else:
            messages.warning(request, 'Please enter valid details.')
            form = forms.BlogForm()
            context['blog_form'] = form

        return render(request, 'blog/blog_update.html', context)


class BlogDeleteView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        blog = models.BlogModel.objects.get(id=self.kwargs['pk'])
        blog.delete()
        messages.success(request, "Deleted Successfully")
        return redirect('blog_list')

