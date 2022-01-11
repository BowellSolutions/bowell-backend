from rest_framework import serializers
from celery.states import PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
from recordings.serializers import RecordingAfterAnalysisSerializer


class InferenceResponseSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=36)
    status = serializers.ChoiceField(choices=(
        PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
    ))
    result = RecordingAfterAnalysisSerializer(required=False)
