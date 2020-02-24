from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Permission)
