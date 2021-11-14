from django.conf import settings
from django.db import models


class Recording(models.Model):
    file = models.FileField(upload_to='recordings') #dopytac sie adama
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    latest_analysis_date = models.DateTimeField(auto_now=True, default=None) #must be called explicitly
    results = models.BinaryField(default=None)

    def __str__(self):
        return f'{self.name} ({self.id})'

'''uploaded_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )'''
