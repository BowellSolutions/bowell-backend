"""
author: Hubert Decyusz

description: File registers Examination model and its model admin with custom model form in admin interface.
"""
from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model

from .models import Examination

User = get_user_model()


class ExaminationModelForm(forms.ModelForm):
    """Examination form with filtered doctor and patient choice fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filter doctors and patients
        self.fields['doctor'].queryset = User.objects.doctors()
        self.fields['patient'].queryset = User.objects.patients()

    class Meta:
        model = Examination
        fields = "__all__"


class ExaminationAdmin(admin.ModelAdmin):
    form = ExaminationModelForm


admin.site.register(Examination, ExaminationAdmin)
