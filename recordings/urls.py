"""
author: Wojciech Nowicki
description: File registers api endpoints
for model methods usage.
"""

from rest_framework.routers import SimpleRouter
from .views import RecordingViewSet

router = SimpleRouter()
router.register(r'recordings', RecordingViewSet, basename='recordings')

urlpatterns = router.urls
