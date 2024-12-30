import re
from django.core.exceptions import ValidationError


def iranian_phone_number_validator(value):
    if not re.match(r'^09\d{9}$', value):
        raise ValidationError(
            'The phone number must be a valid Iranian cellphone number (e.g., 09123456789).')
