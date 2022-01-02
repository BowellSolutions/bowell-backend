"""
author: Hubert Decyusz
description: File consists of viewset definition
used for correct data flow input and output by
mapping usage of correct endpoints, http methods
and serializers, based on taken actions.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Examination
from .serializers import ExaminationSerializer, ExaminationCreateSerializer, ExaminationUpdateSerializer

User = get_user_model()


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
        elif self.request.user.type == "DOCTOR":
            return Examination.objects.filter(doctor=self.request.user)
        elif self.request.user.type == "PATIENT":
            return Examination.objects.filter(patient=self.request.user)
        return Examination.objects.none()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return ExaminationCreateSerializer
        elif hasattr(self, 'action') and self.action in ('update', 'partial_update'):
            return ExaminationUpdateSerializer
        return super().get_serializer_class()


class GetDoctorStatistics(APIView):
    """
        GET     /api/statistics/ - get doctor stats
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.type != "DOCTOR":
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        examination_pending = Examination.objects.filter(doctor=self.request.user).exclude(
            status__in=["cancelled", "processing_succeeded"]).count()
        patients_related = Examination.objects.filter(doctor=self.request.user).distinct("patient").count()
        examination_next_week = Examination.objects.filter(
            doctor=self.request.user, date__gte=timezone.now(),
            date__lte=timezone.now() + timedelta(days=7)).exclude(
            status__in=["cancelled", "processing_succeeded"]
        ).count()
        examinaton_count = Examination.objects.filter(doctor=self.request.user).count()
        return Response({'examinaton_count': examinaton_count,
                         'patients_related_count': patients_related,
                         'examinations_scheduled_count': examination_pending,
                         'examinations_next_week_count': examination_next_week},
                        status=status.HTTP_200_OK)
