from django.http import HttpResponse
from django.shortcuts import redirect,render, render_to_response
from django.template import loader, RequestContext
from users.models import UserProfile
from itemranker.models import MasterList

# Create your views here.


def index(request):
    return render(request, "landing/index-new.html")


def directories(request):
    master_lists = MasterList.objects.all()
    user_profiles = UserProfile.objects.all()
    return render(request, "landing/directories.html", {'master_lists': master_lists, 'user_profiles': user_profiles})


def handler404(request, *args, **argv):
    response = render_to_response('errors/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('errors/404.html')
    response.status_code = 500
    return response
