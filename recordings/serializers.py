from rest_framework import serializers
from .models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Recording
        fields = ('file', 'name', 'uploaded_by')
