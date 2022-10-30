from django.urls import include, path
from . import views
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.ProfilePage.as_view(), name='profile_page'),
    path("resume/", views.ResumePage.as_view(), name='resume_page'),
    path("contacts/", views.ContactsPage.as_view(), name='contacts_page'),
    path("blog/", login_required(views.BlogPage.as_view()), name='blog_page'),
    path("login/", views.login_request, name='login'),
    path("user_create/", views.UserCreateView.as_view(), name='user_create'),
    path("blog-list/", views.BlogListView.as_view(), name='blog_list'),
    path("blog-list/<str:pk>/", views.BlogDetailView.as_view(), name='blog_detail'),
    path("blog-list/update/<str:pk>/", views.BlogUpdateView.as_view(), name='blog_update'),
    path("blog-list/delete/<str:pk>/", views.BlogDeleteView.as_view(), name='blog_delete'),

]
