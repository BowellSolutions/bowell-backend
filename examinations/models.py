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

description: File contains model description of Examination class including relations,
attribute types and constraints which are reflected in database table, and examination_date_validator used
by the model itself.

models:
    - Examination
"""
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from recordings.models import Recording
from django.conf import settings


def examination_date_validator(value):
    """Raises ValidationError if the given date is not in the future."""

    current_date = timezone.now()
    if value < current_date:
        raise ValidationError('Invalid date! Examination date cannot be in the past.')


class Examination(models.Model):
    class Statuses(models.TextChoices):
        cancelled = "cancelled", "cancelled"
        scheduled = "scheduled", "scheduled"
        completed = "completed", "completed"
        file_uploaded = "file_uploaded", "file_uploaded"
        file_processing = "file_processing", "file_processing"
        processing_failed = "processing_failed", "processing_failed"
        processing_succeeded = "processing_succeeded", "processing_succeeded"

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

    date = models.DateTimeField(validators=[examination_date_validator])
    overview = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=40, default='scheduled', choices=Statuses.choices)
    height_cm = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True,
                                            null=True)
    mass_kg = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True,
                                          null=True)
    symptoms = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)

    # celery task id
    analysis_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        db_table = 'examinations'

    def __str__(self):
        return f"Examination {self.id}: {self.status}"
