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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from .models import Examination
from .serializers import (
    ExaminationSerializer,
    ExaminationCreateSerializer,
    ExaminationUpdateSerializer
)
from .swagger import DoctorStatisticsResponse

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

    @swagger_auto_schema(responses={
        HTTP_201_CREATED: openapi.Response('OK', ExaminationSerializer)}
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={
        HTTP_200_OK: openapi.Response('OK', ExaminationSerializer)}
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={
        HTTP_200_OK: openapi.Response('OK', ExaminationSerializer)}
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)


class GetDoctorStatistics(APIView):
    """
    GET     /api/statistics/ - get doctor statistics (examinations and patients count)
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={
        HTTP_200_OK: openapi.Response('OK', DoctorStatisticsResponse),
        HTTP_403_FORBIDDEN: "Permission denied!"
    })
    def get(self, request: Request, *args, **kwargs) -> Response:
        if self.request.user.type != "DOCTOR":
            return Response({'message': 'Permission denied!'}, status=HTTP_403_FORBIDDEN)

        excluded_statuses = ["cancelled", "processing_succeeded"]

        examination_pending = Examination.objects.filter(doctor=self.request.user).exclude(
            status__in=excluded_statuses
        ).count()

        patients_related = Examination.objects.filter(doctor=self.request.user).distinct("patient").count()

        examination_next_week = Examination.objects.filter(
            doctor=self.request.user, date__gte=timezone.now(),
            date__lte=timezone.now() + timedelta(days=7)
        ).exclude(status__in=excluded_statuses).count()

        examination_count = Examination.objects.filter(doctor=self.request.user).count()

        return Response(
            {
                'examination_count': examination_count,
                'patients_related_count': patients_related,
                'examinations_scheduled_count': examination_pending,
                'examinations_next_week_count': examination_next_week
            },
            status=HTTP_200_OK
        )
