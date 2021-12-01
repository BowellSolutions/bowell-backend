"""
author: Hubert Decyusz
description: File describes properties
of model for database table reflection which are
primary key and used table name.
"""

from django.apps import AppConfig


class ExaminationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'examinations'
