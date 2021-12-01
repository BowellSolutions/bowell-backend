"""
author: Hubert Decyusz
description: File registers Examination
model in django content registry.
"""

from django.contrib import admin
from .models import Examination

admin.site.register([Examination])

