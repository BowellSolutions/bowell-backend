from django.urls import path
from .views import RecordingUploadViewSet

urlpatterns = [
    path('recordings/upload', RecordingUploadViewSet.as_view({'put': 'create'}))
]
