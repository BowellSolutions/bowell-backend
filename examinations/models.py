from django.db import models
from recordings.models import Recording
from django.conf import settings


class Examination(models.Model):
    patient = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='patient')
    doctor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='doctor')
    recording = models.ForeignKey(
        to=Recording,
        on_delete=models.SET_NULL,
        null=True)
    examination_date = models.DateTimeField(auto_now_add=True)
    examination_overview = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'examinations'
