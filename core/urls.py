from django.urls import include, path
from . import views
from django.contrib import admin
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.ProfilePage.as_view(), name='profile_page'),
    path("resume/", views.ResumePage.as_view(), name='resume_page'),
    path("contacts/", views.ContactsPage.as_view(), name='contacts_page'),
]
