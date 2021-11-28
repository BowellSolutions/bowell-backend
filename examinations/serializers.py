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
        fields = ('file', 'name')


class ExaminationSerializer(serializers.ModelSerializer):
    patient = UserInfoSerializer()
    doctor = UserInfoSerializer()
    recording = RecordingInExaminationSerializer()

    class Meta:
        model = Examination
        fields = ('id', 'patient', 'height_cm', 'mass_kg', 'symptoms', 'medication',
                  'doctor', 'status', 'recording', 'date', 'overview')


class ExaminationCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True))

    def to_representation(self, instance):
        return ExaminationSerializer(instance).data

    class Meta:
        model = Examination
        fields = ('doctor', 'date')


class ExaminationUpdateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=False))
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Examination
        fields = ('patient', 'height_cm', 'mass_kg', 'symptoms', 'medication', 'doctor', 'status', 'recording', 'overview')


class ExaminationDetailSerializer(serializers.ModelSerializer):
    patient = UserInfoSerializer()

    class Meta:
        model = Examination
        fields = ('id', 'patient', 'height_cm', 'mass_kg', 'symptoms', 'medication', 'status', 'date', 'overview')
