from rest_framework import serializers
from .models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Recording
        fields = ('file', 'name',)
