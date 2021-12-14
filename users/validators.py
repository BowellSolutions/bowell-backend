"""
author: Adam Lisichin
description: File consists of validators' definitions used in models.py.
"""
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

username_validator = UnicodeUsernameValidator()


def birth_date_validator(value):
    """Raises ValidationError if the given date is not in the past."""

    current_date = timezone.now().date()
    if value >= current_date:
        raise ValidationError('Invalid date! Birth date cannot be in the future.')
