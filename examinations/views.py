# ----------------------------------------------
# author: Hubert Decyusz
# description: File consists of viewset definition
# used for correct data flow input and output by
# mapping usage of correct endpoints, http methods
# and serializers, based on taken actions.

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Examination
from .serializers import ExaminationSerializer, ExaminationCreateSerializer, ExaminationUpdateSerializer


class ExaminationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/examinations/          - list all examinations
    POST    /api/examinations/          - register new examination
    GET     /api/examinations/<int:id>/ - retrieve examination
    PUT     /api/examinations/<int:id>/ - update examination
    PATCH   /api/examinations/<int:id>/ - partially update examination
    """

    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Examination.objects.none()
        elif self.request.user.is_staff:
            return Examination.objects.filter(doctor=self.request.user)
        else:
            return Examination.objects.filter(patient=self.request.user)

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return ExaminationCreateSerializer
        elif hasattr(self, 'action') and self.action in ('update', 'partial_update'):
            return ExaminationUpdateSerializer
        return super().get_serializer_class()

