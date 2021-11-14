from django.db import models
from recordings.models import Recording
from users.models import User
# Create your models here.
class Examination(models.Model):
    #id jest sztuczne
    patient_id = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True)
    doctor_id = models.ForeignKey(
                to=User,
                on_delete=models.SET_NULL,
                null=True)
    recording_id = models.ForeignKey(
                to=Recording,
                on_delete=models.SET_NULL,
                null=True)
    examination_date = models.DateTimeField(auto_now_add=True)
    examination_overview = models.TextField(null=True)
    #czy wyniki tu czy w recordings?
