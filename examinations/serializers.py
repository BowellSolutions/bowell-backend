"""
author: Hubert Decyusz
description: File consists of serializers definition
used for correct data flow by using correct attributes
from Examination model which can be used to perform
different operations on particular object.

Used serializers:

UserInfoSerializer - patient/doctor info
RecordingInExaminationSerializer - recording info
ExaminationSerializer - list of examinations
ExaminationCreateSerializer - Examination object creation
ExaminationUpdateSerializer - Examination object update
ExaminationDetailSerializer - full examination info
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
                  'doctor', 'status', 'recording', 'date', 'overview')


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
            examination = Examination.objects.filter(recording=validated_data['recording'])
            if examination.exists():
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
        fields = ('id', 'patient', 'height_cm', 'mass_kg', 'symptoms', 'medication', 'status', 'date', 'overview')
