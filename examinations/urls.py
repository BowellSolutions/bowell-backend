"""
author: Hubert Decyusz
description: File registers api endpoints
for model methods usage.
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ExaminationViewSet, GetDoctorStatistics

router = SimpleRouter()
router.register(r'examinations', ExaminationViewSet, basename='examinations')

urlpatterns = [
    path('statistics/',GetDoctorStatistics.as_view()),
    *router.urls
]
