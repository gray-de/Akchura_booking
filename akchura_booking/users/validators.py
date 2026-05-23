from django.core.exceptions import ValidationError


def validate_capitalized(value):
    if value and value[0].islower():
        raise ValidationError(
            'Имя/фамилия должны начинаться с заглавной буквы.')
