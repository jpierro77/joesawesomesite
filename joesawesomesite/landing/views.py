from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.template import loader
from users.models import UserProfile
from itemranker.models import MasterList

# Create your views here.


def index(request):
    return render(request, "landing/index-new.html")


def directories(request):
    master_lists = MasterList.objects.all()
    user_profiles = UserProfile.objects.all()
    return render(request, "landing/directories.html", {'master_lists': master_lists, 'user_profiles': user_profiles})