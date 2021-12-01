"""
author: Hubert Decyusz
description: File consists of serializers definition
used for correct data flow by using correct attributes
from Recording model which can be used to perform
different operations on particular object.

Used serializers:

ExaminationsFilteredPrimaryKeyRelatedField - logged user related examinations
RecordingCreateSerializer - recording creation
RecordingAfterAnalysisSerializer - full recording model definition also used for update
RecordingBeforeAnalysisSerializer - quick summary of object
ListRecordingsBeforeAnalysisSerializer - list of uploaded recordings
"""

from rest_framework import serializers
from examinations.models import Examination
from .models import Recording
from examinations.serializers import ExaminationDetailSerializer


class ExaminationsFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(ExaminationsFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(doctor=request.user)


class RecordingCreateSerializer(serializers.ModelSerializer):
    examination = ExaminationsFilteredPrimaryKeyRelatedField(queryset=Examination.objects)

    @property
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def to_representation(self, instance):
        return RecordingBeforeAnalysisSerializer(instance).data

    def create(self, validated_data):
        instance = super().create(validated_data)
        examination = validated_data.get('examination')
        if examination.recording is not None:
            raise serializers.ValidationError(
                {'detail': 'Another recording has already been assigned to chosen examination.'})
        else:
            examination.recording = instance
            examination.save()
        return instance

    class Meta:
        model = Recording

        fields = ('file', 'name', 'examination')


class RecordingAfterAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        exclude = ('file', 'name')


class RecordingBeforeAnalysisSerializer(serializers.ModelSerializer):
    examination = serializers.SerializerMethodField('get_examinations')

    @property
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    # todo return if examination does not exists
    def get_examinations(self, obj):
        return ExaminationDetailSerializer(obj.examination_set.first()).data

    class Meta:
        model = Recording
        fields = ('id', 'file', 'name', 'uploaded_at', 'examination')


class ListRecordingsBeforeAnalysisSerializer(serializers.ModelSerializer):
    examination = serializers.SerializerMethodField('get_examinations')

    @property
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def get_examinations(self, obj):
        if obj.examination_set.first():
            return ExaminationDetailSerializer(obj.examination_set.first()).data
        return None

    class Meta:
        model = Recording
        fields = ('id', 'file', 'name', 'uploaded_at', 'examination')
