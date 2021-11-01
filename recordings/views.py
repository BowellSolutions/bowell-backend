from rest_framework import mixins, viewsets

from .serializers import RecordingSerializer


class RecordingUploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RecordingSerializer
