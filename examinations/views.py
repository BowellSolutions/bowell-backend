"""
authors: Hubert Decyusz, Wojciech Nowicki, Adam Lisichin

description: File consists of viewset definition used for correct data flow input and output by
mapping usage of correct endpoints, http methods and serializers, based on taken actions.

Defined views and viewsets:
    - ExaminationViewSet - examination CRUD
    - GetDoctorStatistics - doctor statistics
"""
from datetime import timedelta

from celery.result import AsyncResult
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView

from analysis.swagger import InferenceResponseSerializer
from analysis.tasks import process_recording
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'patient']

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
        elif hasattr(self, 'action') and self.action == "inference":
            return Serializer  # empty serializer
        return super().get_serializer_class()

    @swagger_auto_schema(responses={HTTP_201_CREATED: openapi.Response('OK', ExaminationSerializer)})
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={HTTP_200_OK: openapi.Response('OK', ExaminationSerializer)})
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={HTTP_200_OK: openapi.Response('OK', ExaminationSerializer)})
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(method="GET", responses={
        HTTP_200_OK: openapi.Response('Checked task state', InferenceResponseSerializer),
        HTTP_403_FORBIDDEN: openapi.Response('Permission denied!')
    })
    @swagger_auto_schema(method="POST", responses={
        HTTP_200_OK: openapi.Response('Analysis has been started'),
        HTTP_403_FORBIDDEN: openapi.Response('Permission denied!')
    })
    @action(detail=True, methods=['GET', 'POST'])
    def inference(self, request, *args, **kwargs):
        examination: Examination = self.get_object()
        recording = examination.recording

        # check if there is recording attached
        if not recording:
            return Response({"message": "Permission denied!"}, status=HTTP_404_NOT_FOUND)

        if request.method == "POST":
            # check if user is a doctor and if examination belongs to them - only doctor can start inference
            if request.user.type != User.Types.DOCTOR or examination.doctor != request.user:
                return Response({"message": "Permission denied!"}, status=HTTP_403_FORBIDDEN)

            # run celery task
            task = process_recording.delay(recording.id, recording.file.path, request.user.id)
            return Response(
                {"message": f"Analysis of Recording ({recording.id}) has been started!", "task_id": task.id},
                status=HTTP_200_OK
            )
        else:
            # check if user is either doctor or patient in this examination
            if examination.doctor != request.user and examination.patient != request.user:
                return Response({"message": "Permission denied!"}, status=HTTP_403_FORBIDDEN)

            task_id = examination.analysis_id
            if not task_id:
                return Response(
                    {"message": f"This examination does not have analysis_id set!"}, status=HTTP_400_BAD_REQUEST
                )

            # check task status in celery backend
            task = AsyncResult(task_id)
            result = task.result if task.status == "SUCCESS" else None

            return Response(
                {"task_id": task.task_id, "status": task.status, "result": result}, status=HTTP_200_OK
            )


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
