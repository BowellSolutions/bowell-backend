"""
author: Hubert Decyusz, Wojciech Nowicki

description: File registers API endpoints

endpoints:
    - /api/examinations/
    - /api/examinations/<id>/
    - /api/examinations/<id>/inference
    - /api/statistics/
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ExaminationViewSet, GetDoctorStatistics

router = SimpleRouter()
router.register(r'examinations', ExaminationViewSet, basename='examinations')

urlpatterns = [
    path('statistics/', GetDoctorStatistics.as_view()),
    *router.urls
]
