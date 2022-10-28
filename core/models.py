from mptt.models import MPTTModel
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, User
from froala_editor.fields import FroalaField

class Role(MPTTModel):
    name = models.CharField(max_length=64, blank=False, unique=True,
                            error_messages={'unique': "This name already exists.", }, )
    group = models.ForeignKey(Group, blank=False, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.name)


class Profile(MPTTModel, AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=10, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'mobile'

    def __str__(self):
        return "{}".format(self.user if self.user else "")

class BlogModel(models.Model):
    title = models.CharField(max_length=50)
    content =FroalaField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=100)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.title)
