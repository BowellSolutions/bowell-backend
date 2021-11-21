from django.conf import settings
from django.db import models


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls


@auto_str
class Recording(models.Model):
    file = models.FileField(upload_to='recordings')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    latest_analysis_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # main results
    length = models.DurationField(blank=True, null=True)
    bowell_sounds_number = models.PositiveIntegerField(blank=True, null=True)
    bowell_sounds_per_minute = models.FloatField(blank=True, null=True)
    # frequency analysis in three-minute periods
    mean_per_minute = models.FloatField(blank=True, null=True)
    deviation_per_minute = models.FloatField(blank=True, null=True)
    median_per_minute = models.FloatField(blank=True, null=True)
    first_quartile_per_minute = models.FloatField(blank=True, null=True)
    third_quartile_per_minute = models.FloatField(blank=True, null=True)
    first_decile_per_minute = models.FloatField(blank=True, null=True)
    ninth_decile_per_minute = models.FloatField(blank=True, null=True)
    minimum_per_minute = models.FloatField(blank=True, null=True)
    maximum_per_minute = models.FloatField(blank=True, null=True)
    # Duration analysis, individual bowel sounds
    mean = models.FloatField(blank=True, null=True)
    deviation = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    first_quartile = models.FloatField(blank=True, null=True)
    third_quartile = models.FloatField(blank=True, null=True)
    first_decile = models.FloatField(blank=True, null=True)
    ninth_decile = models.FloatField(blank=True, null=True)
    minimum = models.FloatField(blank=True, null=True)
    maximum = models.FloatField(blank=True, null=True)
    rmssd = models.FloatField(blank=True, null=True)
    rmssd_logarithm = models.FloatField(blank=True, null=True)
    sdnn = models.FloatField(blank=True, null=True)
    # Sound analysis total
    sound_index = models.FloatField(blank=True, null=True)
    # sound analysis per minute
    # technical details
    similarity_to_training_set = models.FloatField(blank=True, null=True)
