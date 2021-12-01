from time import sleep

from celery import shared_task

from analysis.celery import app
from recordings.models import Recording


@shared_task
def simple_task(x: int, y: int):
    sleep(1)
    return x + y


model_mock = {
    'bowell_sounds_number': 1.0,
    'bowell_sounds_per_minute': 2.0,
    # frequency analysis in three-minute periods
    'mean_per_minute': 3.0,
    'deviation_per_minute': 4.0,
    'median_per_minute': 5.0,
    'first_quartile_per_minute': 6.0,
    'third_quartile_per_minute': 7.0,
    'first_decile_per_minute': 8.0,
    'ninth_decile_per_minute': 9.0,
    'minimum_per_minute': 10.0,
    'maximum_per_minute': 11.0,
    'repetition_within_50ms': 12.0,
    'repetition_within_100ms': 13.0,
    'repetition_within_200ms': 14.0,
    'containing_30s_periods_percentage': 2.0,
    # Duration analysis, individual bowel sounds
    'mean': 2.0,
    'deviation': 2.0,
    'median': 2.0,
    'first_quartile': 2.0,
    'third_quartile': 2.0,
    'first_decile': 2.0,
    'ninth_decile': 2.0,
    'minimum': 2.0,
    'maximum': 2.0,
    'rmssd': 2.0,
    'rmssd_logarithm': 2.0,
    'sdnn': 2.0,
    'porta_index': 2.0,
    'guzik_index': 2.0,
    'high_frequency_power': 2.0,
    'medium_frequency_power': 2.0,
    'low_frequency_power': 2.0,
    # Sound analysis total
    'total_sound_index': 2.0,
    'total_sound_duration': 2.0,
    # sound analysis per three minute periods
    'total_sound_index_per_3minutes': 2.0,
    'total_sound_duration_per_3minutes': 2.0,
    # technical details
    'similarity_to_training_set': 2.0,
}


@app.task
def process_recording(recording_id: int):
    recording = Recording.objects.filter(id=recording_id).update(**model_mock)
    return recording
