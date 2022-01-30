"""
Copyright (c) 2022 Adam Lisichin, Hubert Decyusz, Wojciech Nowicki, Gustaw Daczkowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

author: Hubert Decyusz

description: File consists of serializers definition used for correct data flow by using correct attributes
from Recording model which can be used to perform different operations on particular object.

custom serializer fields:
    - ExaminationsFilteredPrimaryKeyRelatedField - logged user related examinations

serializers:
    - RecordingCreateSerializer - recording creation
    - RecordingAfterAnalysisSerializer - full recording model definition also used for update
    - RecordingBeforeAnalysisSerializer - quick summary of object
    - ListRecordingsBeforeAnalysisSerializer - list of uploaded recordings
"""

from rest_framework import serializers

from examinations.models import Examination
from examinations.serializers import ExaminationDetailSerializer
from .models import Recording


class ExaminationsFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """PrimaryKeyRelatedField with queryset filtered by current doctor"""

    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(ExaminationsFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(doctor=request.user)


class RecordingCreateSerializer(serializers.ModelSerializer):
    """Serializer used for creating new recording"""
    examination = ExaminationsFilteredPrimaryKeyRelatedField(queryset=Examination.objects)

    @property
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def to_representation(self, instance):
        return RecordingBeforeAnalysisSerializer(instance).data

    def create(self, validated_data):
        examination = validated_data.get('examination')
        if examination.recording is not None:
            raise serializers.ValidationError(
                {'detail': 'Another recording has already been assigned to chosen examination.'})
        else:
            validated_data['uploader'] = self._user
            instance = super().create(validated_data)
            examination.recording = instance
            examination.status = Examination.Statuses.file_uploaded
            examination.save()
        return instance

    class Meta:
        model = Recording
        fields = ('file', 'name', 'examination')


class RecordingAfterAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for recording representation and updates"""
    uploader = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recording
        exclude = ('file', 'name')


class RecordingBeforeAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for recording representation before analysis"""
    examination = serializers.SerializerMethodField('get_examinations')

    def get_examinations(self, obj):
        return ExaminationDetailSerializer(obj.examination_set.first()).data

    class Meta:
        model = Recording
        fields = ('id', 'file', 'name', 'uploaded_at', 'examination', 'uploader')


class ListRecordingsBeforeAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for recording representation in list method"""
    examination = serializers.SerializerMethodField('get_examinations')

    def get_examinations(self, obj):
        if obj.examination_set.first():
            return ExaminationDetailSerializer(obj.examination_set.first()).data
        return None

    class Meta:
        model = Recording
        fields = ('id', 'file', 'name', 'uploaded_at', 'examination', 'uploader')
