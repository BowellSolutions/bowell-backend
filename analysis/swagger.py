"""
author: Adam Lisichin

description: File consists of serializers definition used only for swagger documentation.
"""
from rest_framework import serializers
from celery.states import PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
from recordings.serializers import RecordingAfterAnalysisSerializer


class InferenceResponseSerializer(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at GET /api/examinations/<id>/inference/"""
    task_id = serializers.CharField(max_length=36)
    status = serializers.ChoiceField(choices=(
        PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
    ))
    # optional result
    result = RecordingAfterAnalysisSerializer(required=False)
