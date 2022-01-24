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
from Examination model which can be used to perform different operations on particular object.

serializers:
    - UserInfoSerializer - patient/doctor info
    - RecordingInExaminationSerializer - recording info
    - ExaminationSerializer - list of examinations
    - ExaminationCreateSerializer - Examination object creation
    - ExaminationUpdateSerializer - Examination object update
    - ExaminationDetailSerializer - full examination info
"""
from rest_framework import serializers
from .models import Examination, Recording
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class RecordingInExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ('id', 'file', 'name')


class ExaminationSerializer(serializers.ModelSerializer):
    patient = UserInfoSerializer()
    doctor = UserInfoSerializer()
    recording = RecordingInExaminationSerializer()

    class Meta:
        model = Examination
        fields = ('id', 'patient', 'height_cm', 'mass_kg', 'symptoms', 'medication',
                  'doctor', 'status', 'recording', 'date', 'overview', 'analysis_id')


class ExaminationCreateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(type=User.Types.PATIENT))
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(type=User.Types.DOCTOR))

    def to_representation(self, instance):
        return ExaminationSerializer(instance).data

    class Meta:
        model = Examination
        fields = ('patient', 'doctor', 'date')


class ExaminationUpdateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(type=User.Types.PATIENT))
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(type=User.Types.DOCTOR))

    def update(self, instance, validated_data):
        if 'recording' in validated_data:
            # if examination already has a recording
            # or recording from request is already attached elsewhere
            if instance.recording is not None or Examination.objects.filter(
                    recording=validated_data['recording']).exists():
                raise serializers.ValidationError(
                    {'detail': 'Another recording has already been assigned to chosen examination.'})

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return ExaminationSerializer(instance).data

    class Meta:
        model = Examination
        fields = (
            'patient', 'height_cm', 'mass_kg', 'symptoms', 'medication', 'doctor', 'status', 'recording', 'overview'
        )


class ExaminationDetailSerializer(serializers.ModelSerializer):
    patient = UserInfoSerializer()

    class Meta:
        model = Examination
        fields = (
            'id',
            'patient',
            'height_cm',
            'mass_kg',
            'symptoms',
            'medication',
            'status',
            'date',
            'overview',
            'analysis_id',
        )
