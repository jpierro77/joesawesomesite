from django import forms
from django.core.validators import RegexValidator

no_symbols = RegexValidator(r'^[0-9a-zA-Z ]*$', 'No symbols allowed')
m_or_f = RegexValidator(r'^[m|f]*', "must be male or female")


class UserHealthInfo(forms.Form):
    weight = forms.IntegerField()
    height = forms.IntegerField()
    age = forms.IntegerField()
    gender = forms.CharField(max_length=1, validators=[m_or_f])
    lbs_per_week_goal = forms.IntegerField()
    activity_level = forms.FloatField(min_value=1.3, max_value=2.0)


class Food(forms.Form):
    food_name = forms.CharField(max_length=100, validators=[no_symbols])
    food_calories = forms.IntegerField()