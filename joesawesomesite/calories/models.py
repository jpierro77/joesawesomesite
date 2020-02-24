from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.


class Day(models.Model):
    date = models.DateField('Date')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.IntegerField('Daily Limit')
    foods = models.TextField('Food List')

    def __str__(self):
        return f'{self.user.username}\'s  {self.date}'

    def total_calories(self):
        total = 0
        for food in json.loads(self.foods)['foods']:
            total += int(food['calories'])

        return total


class UserHealthInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField('Current Weight')
    gender = models.CharField('Gender', max_length=1)
    height = models.IntegerField('Height')
    age = models.IntegerField('Age')
    lbs_per_week_goal = models.IntegerField("Pounds Per Week", default=0)
    activity_level = models.FloatField('Activity Level')

    def get_bmr(self):
        kg_weight = self.weight / 2.205
        cm_height = self.height * 2.54

        if self.gender == "m":
            return (66.4730 +
                    (13.7516 * kg_weight) +
                    (5.003 * cm_height) -
                    (6.7550 * self.age))
        elif self.gender == "f":
            return (655.0955 +
                    (9.5634 * kg_weight) +
                    (1.8496 * cm_height) -
                    (4.6756 * self.age))
        else:
            return False

    def calculate_limit(self):
        return ((self.get_bmr() * self.activity_level) +
                (500 * self.lbs_per_week_goal))

    def __str__(self):
        return f'{self.user.username}\'s Health Info'


class DateMethods:
    def __init__(self, days, date):
        self.current_date = date
        self.year_num = date.year
        self.day = date.day
        self.month_num = date.month
        self.days = days
        num_days = 28

        if self.year_num % 4 == 0:
            if self.year_num % 100 == 0:
                if self.year_num % 400 == 0:
                    num_days = 29
                else:
                    num_days = 28
            else:
                num_days = 29
        else:
            num_days = 28
        self.months = [
            {'name': 'january', 'num_days': '30'},
            {'name': 'february', 'num_days': num_days},
            {'name': 'march', 'num_days': '31'},
            {'name': 'april', 'num_days': '30'},
            {'name': 'may', 'num_days': '31'},
            {'name': 'june', 'num_days': '30'},
            {'name': 'july', 'num_days': '31'},
            {'name': 'august', 'num_days': '31'},
            {'name': 'september', 'num_days': '30'},
            {'name': 'october', 'num_days': '31'},
            {'name': 'november', 'num_days': '30'},
            {'name': 'december', 'num_days': '31'},
        ]

    def days_tracked(self):
        counter = 0
        under_limit_counter = 0
        for day in self.days:
            if day.date.month == self.month_num:
                counter += 1
                if day.total_calories() < day.limit:
                    under_limit_counter += 1
        print(under_limit_counter)
        return{
            'days_tracked': counter,
            'days_under_limit': under_limit_counter,
            'days_in_month': int(self.months[self.month_num - 1]['num_days']),
            'days_remaining': int(self.months[self.month_num - 1]['num_days'])-int(self.day),
        }