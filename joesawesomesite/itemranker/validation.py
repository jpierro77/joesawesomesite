from django.core.validators import RegexValidator

no_symbols = RegexValidator(r'^[0-9a-zA-Z ]*$', 'No symbols allowed')
master_or_personal = RegexValidator(r'^[master|personal]*', "must be master or personal")

