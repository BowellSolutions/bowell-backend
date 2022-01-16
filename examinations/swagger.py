"""
author: Adam Lisichin

description: File consists of serializers definition used only for swagger documentation.

serializers:
    - DoctorStatisticsResponse
"""
from rest_framework import serializers


class DoctorStatisticsResponse(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at POST /api/statistics/"""
    examination_count = serializers.IntegerField(min_value=0)
    patients_related_count = serializers.IntegerField(min_value=0)
    examinations_scheduled_count = serializers.IntegerField(min_value=0)
    examinations_next_week_count = serializers.IntegerField(min_value=0)

    def create(self, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Implementation required by abstract base class"""
        raise NotImplementedError()
