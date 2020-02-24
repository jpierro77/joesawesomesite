from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Day, UserHealthInfo, DateMethods
import datetime
import json

from django.contrib.auth.models import User

# Create your views here.


def index(request):
    if 'from_calories' in request.session.keys():
        del request.session['from_calories']

    user = User.objects.filter(username=request.user.username).first()
    if request.user.is_authenticated and hasattr(user, 'userhealthinfo'):
        days = Day.objects.filter(user=int(user.id))
        date_methods = DateMethods(days, datetime.date.today())
        tracked = date_methods.days_tracked()
        print("You\'ve tracked" +
              str(tracked['days_tracked']) +
              " out of " + str(tracked['days_in_month']) +
              " days this month. " +
              str(tracked['days_remaining']) +
              " days remaining")
        counter = 0

        day_string = "{\"content\":{ \"days\":["
        for day in days:
            day_string += str(day.foods)
            counter += 1
            if counter < len(days):
                day_string += ","

        day_string += "]}}"
        health_info = user.userhealthinfo
        daily_limit = user.userhealthinfo.calculate_limit()
        print(daily_limit)
        return render(request, 'calories/index.html',
                      {'data': health_info, 'daily_limit': int(daily_limit), 'days': day_string})
    else:
        return render(request, 'calories/index.html')


def update_health_info(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()

        if "health_info" in request.session.keys():
            posted_health_info = request.session["health_info"]
            del request.session['health_info']
        elif request.method == "POST":
            posted_health_info = request.POST

        if not hasattr(user, 'userhealthinfo'):
            health_info = UserHealthInfo()
            health_info.user = user
        else:
            health_info = user.userhealthinfo

        try:
            health_info.weight = posted_health_info['weight']
            health_info.height = posted_health_info['height']
            health_info.activity_level = posted_health_info['activity_level']
            health_info.age = posted_health_info['age']
            health_info.gender = posted_health_info['gender']
            health_info.lbs_per_week_goal = posted_health_info['lbs_per_week_goal']
            health_info.save()
        except Exception as inst:
            print("Something went wrong:")
            print(inst)
        return redirect("caloriesindex")
    else:
        try:
            request.session["health_info"] = request.POST
        except Exception as inst:
            print(inst)
            return redirect("caloriesindex")
        messages.success(request, f'Please login to create a Health Profile')
        return redirect('login')


def new_day(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        day_info_string = request.POST['day_data']
        date = json.loads(day_info_string)['date']
        day = Day.objects.filter(date=date, user=user).first()
        if day is None:
            day = Day()
        day.date = date
        day.user = user
        day.limit = json.loads(day_info_string)['limit']
        day.foods = day_info_string
        day.save()

    return redirect("caloriesindex")


def login_redirect(request):
    request.session['from_calories'] = True
    messages.success(request, f'Please sign in to create health profile')
    return redirect('login')
