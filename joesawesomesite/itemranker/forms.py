from django import forms
from django.core.validators import RegexValidator

no_symbols = RegexValidator(r'^[0-9a-zA-Z ]*$', 'No symbols allowed')
master_or_personal = RegexValidator(r'^[master|personal]*', "must be master or personal")


class Item(forms.Form):
    rank = forms.IntegerField(required=False)
    item_name = forms.CharField(max_length=200, validators=[no_symbols])
    votes = forms.IntegerField()


class ListDetails(forms.Form):
    list_title = forms.CharField(max_length=200, validators=[no_symbols])
    list_type = forms.CharField(validators=[master_or_personal])


