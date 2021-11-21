from rest_framework import serializers
from .models import Examination, User
from recordings.serializers import RecordingSerializer


class UserInfoField(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'surname')


class ExaminationSerializer(serializers.ModelSerializer):
    patient = UserInfoField()
    doctor = UserInfoField()
    recording = RecordingSerializer()

    class Meta:
        model = Examination
        fields = ('patient', 'doctor', 'recording', 'examination_date', 'examination_overview')
