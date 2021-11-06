from django.contrib.auth.models import User
from django.db import models


class Recording(models.Model):
    file = models.FileField(upload_to='recordings')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} ({self.id})'
