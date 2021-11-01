from django.db import models


class Recording(models.Model):
    file = models.FileField(upload_to='recordings')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
