"""
Copyright (c) 2022 Adam Lisichin, Hubert Decyusz, Wojciech Nowicki, Gustaw Daczkowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

author: Wojciech Nowicki

description: File consists of viewset definition used for correct data flow input and output by
mapping usage of correct endpoints, http methods and serializers, based on taken actions.

views and viewsets:
    - RecordingViewSet - recordings CRUD
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from examinations.models import Examination
from .models import Recording
from .serializers import (
    ListRecordingsBeforeAnalysisSerializer,
    RecordingAfterAnalysisSerializer,
    RecordingCreateSerializer, 
    RecordingBeforeAnalysisSerializer
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
        HTTP_201_CREATED: openapi.Response('OK', RecordingBeforeAnalysisSerializer)}
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={
        HTTP_200_OK: "Recording was successfully detached from examination.",
        HTTP_400_BAD_REQUEST: "Recording was not assigned to any examination."
    })
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        examination_qs = self.get_object().examination_set
        if examination_qs.exists():
            examination = examination_qs.first()
            examination.recording = None
            examination.analysis_id = None
            examination.status = Examination.Statuses.scheduled
            examination.save(update_fields=['recording', 'analysis_id'])
            return Response(
                {'message': 'Recording was successfully detached from examination.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'message': 'Recording was not assigned to any examination.'},
            status=status.HTTP_400_BAD_REQUEST
        )
