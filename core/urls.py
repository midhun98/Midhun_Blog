from django.urls import include, path
from . import views
from django.contrib import admin
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.ProfilePage.as_view(), name='pinned')
]
