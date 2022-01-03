"""
author: Wojciech Nowicki
description: File consists of viewset definition
used for correct data flow input and output by
mapping usage of correct endpoints, http methods
and serializers, based on taken actions.
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Recording
from .serializers import (
    ListRecordingsBeforeAnalysisSerializer,
    RecordingAfterAnalysisSerializer,
    RecordingCreateSerializer
)

User = get_user_model()


class RecordingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/recordings/          - list all recordings
    POST    /api/recordings/          - register new recording
    GET     /api/recordings/<int:id>/ - retrieve recording
    PUT     /api/recordings/<int:id>/ - update recording
    PATCH   /api/recordings/<int:id>/ - partially update recording
    """

    serializer_class = ListRecordingsBeforeAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Recording]:
        if self.request.user.is_anonymous:
            return Recording.objects.none()
        elif self.request.user.type == User.Types.DOCTOR:
            # recordings uploaded by current user (doctor)
            return Recording.objects.filter(uploader=self.request.user)
        return Recording.objects.none()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return RecordingCreateSerializer
        elif hasattr(self, 'action') and self.action in ('update', 'partial_update', 'retrieve'):
            return RecordingAfterAnalysisSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(responses={
        HTTP_200_OK: "Recording was successfully detached from examination.",
        HTTP_400_BAD_REQUEST: "Recording was not assigned to any examination."
    })
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        examination_qs = self.get_object().examination_set
        if examination_qs.exists():
            examination = examination_qs.first()
            examination.recording = None
            examination.save(update_fields=['recording'])
            return Response(
                {'message': 'Recording was successfully detached from examination.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'message': 'Recording was not assigned to any examination.'},
            status=status.HTTP_400_BAD_REQUEST
        )
