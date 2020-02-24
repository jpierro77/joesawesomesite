from django.shortcuts import render
from django.contrib.auth import authenticate, login as userlogin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import UserProfile
from itemranker.models import MasterList, MasterItem, PersonalList

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account created for {username}')
            return redirect('login')
        else:
            messages.error(request, f'Account not created')
        return render(request, 'users/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def edit_profile(request):

    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        personal_lists = PersonalList.objects.filter(user=user)
        master_lists = MasterList.objects.filter(user=user)
        if request.method == "POST":
            if hasattr(user, "userprofile"):
                user.userprofile.first_name = request.POST['first_name']
                user.userprofile.last_name = request.POST['last_name']
                user.userprofile.summary = request.POST['summary']
                user.userprofile.save()
            else:
                profile = UserProfile()
                profile.user = user
                profile.first_name = request.POST['first_name']
                profile.last_name = request.POST['last_name']
                profile.summary = request.POST['summary']
                profile.save()
            messages.success(request, f'Profile Saved')
        return render(request, "users/editprofile.html", {
                'user': user,
                'personal_lists': personal_lists,
                'master_lists': master_lists
            })
    else:
        messages.error(request, f'Please Log In before editing your profile')
        return redirect("login")


def user_profile(request, username=""):
    if username == "":
        user = request.user
    else:
        user = User.objects.filter(username=username).first()
    print(user.id)
    personal_lists = PersonalList.objects.filter(user=user)
    master_lists = MasterList.objects.filter(user=user)
    return render(request, 'users/profilebase.html',
                  {'user': user,
                   'personal_lists': personal_lists,
                   'master_lists': master_lists})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            userlogin(request, user)
            if 'save_data' in request.session.keys():
                return redirect("savelist")
            elif 'health_info' in request.session.keys():
                return redirect('updatehealthinfo')
            elif 'from_calories' in request.session.keys():
                return redirect('caloriesindex')
            else:
                if not UserProfile.objects.filter(id=user.id).exists():
                    messages.success(request,
                                     f'First time log in, please edit your profile')
                    return redirect("edit_profile")
                else:
                    return redirect("index")

        else:
            messages.error(request, f'Invalid username or password')
            return render(request, "users/login.html")
    else:
        return render(request, "users/login.html")