# ----------------------------------------------
# author: Wojciech Nowicki
# description: File consists of viewset definition
# used for correct data flow input and output by
# mapping usage of correct endpoints, http methods
# and serializers, based on taken actions.

from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Recording
from .serializers import ListRecordingsBeforeAnalysisSerializer, RecordingAfterAnalysisSerializer, RecordingCreateSerializer


class RecordingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/recordings/          - list all examinations
    POST    /api/recordings/          - register new recording
    GET     /api/recordings/<int:id>/ - retrieve recording
    PUT     /api/recordings/<int:id>/ - update recording
    PATCH   /api/recordings/<int:id>/ - partially update recording
    """

    serializer_class = ListRecordingsBeforeAnalysisSerializer
    permission_classes = [IsAuthenticated]
    queryset = Recording.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return RecordingCreateSerializer
        elif hasattr(self, 'action') and self.action in ('update', 'partial_update', 'retrieve'):
            return RecordingAfterAnalysisSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
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

