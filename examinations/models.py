"""
author: Hubert Decyusz
description: File contains model description
of Examination class including relations,
attribute types and constraints which are
reflected in database table.
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from recordings.models import Recording
from django.conf import settings

# todo add all statuses
STATUSES = [('forthcoming', 'forthcoming'), ('completed', 'completed'), ('cancelled', 'cancelled')]


class Examination(models.Model):
    patient = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True, related_name='patient')
    doctor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='doctor')
    recording = models.ForeignKey(
        to=Recording,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    date = models.DateTimeField()
    overview = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=40, default='forthcoming', choices=STATUSES)
    height_cm = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True)
    mass_kg = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'examinations'

    def __str__(self):
        return f"Examination {self.id}: {self.status}"

