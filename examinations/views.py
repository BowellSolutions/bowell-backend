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

