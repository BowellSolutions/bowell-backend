"""
author: Wojciech Nowicki
description: File contains model description
of Recording class. Class has no relation dependent
attributes, only those necessary for full model definition.
"""

from django.db import models


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
    repetition_within_50ms = models.FloatField(blank=True, null=True)
    repetition_within_100ms = models.FloatField(blank=True, null=True)
    repetition_within_200ms = models.FloatField(blank=True, null=True)
    containing_30s_periods_percentage = models.FloatField(blank=True, null=True)

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
    porta_index = models.FloatField(blank=True, null=True)
    guzik_index = models.FloatField(blank=True, null=True)
    high_frequency_power = models.FloatField(blank=True, null=True)
    medium_frequency_power = models.FloatField(blank=True, null=True)
    low_frequency_power = models.FloatField(blank=True, null=True)

    # Sound analysis total
    total_sound_index = models.FloatField(blank=True, null=True)
    total_sound_duration = models.FloatField(blank=True, null=True)

    # sound analysis per three minute periods
    total_sound_index_per_3minutes = models.FloatField(blank=True, null=True)
    total_sound_duration_per_3minutes = models.FloatField(blank=True, null=True)

    # technical details
    similarity_to_training_set = models.FloatField(blank=True, null=True)

    # plots
    bowell_sounds_per_minute_in_time = models.BinaryField(blank=True, null=True)
    sound_index_in_time = models.BinaryField(blank=True, null=True)
    sound_duration_in_time = models.BinaryField(blank=True, null=True)
    sounds_per_minute_histogram = models.BinaryField(blank=True, null=True)
    sound_duration_histogram = models.BinaryField(blank=True, null=True)
    sounds_per_minute_vs_sound_index_scatterplot = models.BinaryField(blank=True, null=True)
    sounds_per_minute_vs_sound_duration_scatterplot = models.BinaryField(blank=True, null=True)
    sound_index_vs_duration_scatterplot = models.BinaryField(blank=True, null=True)

