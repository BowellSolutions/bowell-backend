"""
author: Wojciech Nowicki
description: File describes properties
of model for database table reflection which are
primary key and used table name.
"""

from django.apps import AppConfig


class RecordingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recordings'
