# ----------------------------------------------
# author: Wojciech Nowicki
# description: File registers Recording
# model in django content registry.

from django.contrib import admin
from .models import Recording

admin.site.register([Recording])
