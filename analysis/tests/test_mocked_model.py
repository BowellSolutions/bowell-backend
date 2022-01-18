"""
author: Adam Lisichin

description: File contains tests used for analysis app testing.
"""
from unittest import skip

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from analysis.tasks import process_recording, model_mock
from recordings.models import Recording


@override_settings(CELERY_USE_MOCK_MODEL=True)
class TestModelResponse(TestCase):
    def setUp(self):
        self.recording = Recording.objects.create(
            file=SimpleUploadedFile("test.wav", b"file_content", content_type="audio/wav"),
            name="test.wav"
        )

    @skip("Program does not wait for task to finish its execution")
    def test_long_running_mocked_model_response(self):
        task = process_recording.s(self.recording.id, self.recording.file.path).apply()
        self.assertEqual(task.status, 'SUCCESS')
        self.assertEqual(task.result, self.recording.id)
        # get refresh model
        r = Recording.objects.get(id=self.recording.id)
        self.assertDictEqual(
            {
                'bowell_sounds_number': r.bowell_sounds_number,
                'bowell_sounds_per_minute': r.bowell_sounds_per_minute,
                'mean_per_minute': r.mean_per_minute,
                'deviation_per_minute': r.deviation_per_minute,
                'median_per_minute': r.median_per_minute,
                'first_quartile_per_minute': r.first_quartile_per_minute,
                'third_quartile_per_minute': r.third_quartile_per_minute,
                'first_decile_per_minute': r.first_decile_per_minute,
                'ninth_decile_per_minute': r.ninth_decile_per_minute,
                'minimum_per_minute': r.minimum_per_minute,
                'maximum_per_minute': r.maximum_per_minute,
                'repetition_within_50ms': r.repetition_within_50ms,
                'repetition_within_100ms': r.repetition_within_100ms,
                'repetition_within_200ms': r.repetition_within_200ms,
                'containing_30s_periods_percentage': r.containing_30s_periods_percentage,
                'mean': r.mean,
                'deviation': r.deviation,
                'median': r.median,
                'first_quartile': r.first_quartile,
                'third_quartile': r.third_quartile,
                'first_decile': r.first_decile,
                'ninth_decile': r.ninth_decile,
                'minimum': r.minimum,
                'maximum': r.maximum,
                'rmssd': r.rmssd,
                'rmssd_logarithm': r.rmssd_logarithm,
                'sdnn': r.sdnn,
                'porta_index': r.porta_index,
                'guzik_index': r.guzik_index,
                'high_frequency_power': r.high_frequency_power,
                'medium_frequency_power': r.medium_frequency_power,
                'low_frequency_power': r.low_frequency_power,
                'total_sound_index': r.total_sound_index,
                'total_sound_duration': r.total_sound_duration,
                'total_sound_index_per_3minutes': r.total_sound_index_per_3minutes,
                'total_sound_duration_per_3minutes': r.total_sound_duration_per_3minutes,
                'similarity_to_training_set': r.similarity_to_training_set,
            },
            model_mock
        )
