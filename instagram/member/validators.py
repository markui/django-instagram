from django.core.exceptions import ValidationError


# usually use validate_(for general validation not clean_(method in form)
def validate_username(value):
    if value == 'kkh':
        raise ValidationError(f'fuck {value}')

