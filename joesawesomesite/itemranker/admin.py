from django.contrib import admin
from .models import MasterList, PersonalList, MasterItem
# Register your models here.
admin.site.register(MasterList)
admin.site.register(MasterItem)
admin.site.register(PersonalList)