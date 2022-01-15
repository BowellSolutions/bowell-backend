import asyncio
import random

import requests
from asgiref.sync import async_to_sync
from celery import Task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.conf import settings

from analysis.celery import app
from examinations.models import Examination
from examinations.serializers import ExaminationSerializer
from recordings.models import Recording
from recordings.serializers import RecordingAfterAnalysisSerializer

logger = get_task_logger(__name__)

mapper = {
    "% of bowel sounds followed by another bowel sound within 100 ms": "repetition_within_100ms",
    "% of bowel sounds followed by another bowel sound within 200 ms": "repetition_within_200ms",
    "% of bowel sounds followed by another bowel sound within 50 ms": "repetition_within_50ms",
    "Bowel sounds identified, total count": "bowell_sounds_number",
    "Bowel sounds per minute, 1st decile": "first_decile_per_minute",
    "Bowel sounds per minute, 1st quartile": "first_quartile_per_minute",
    "Bowel sounds per minute, 3rd quartile": "third_quartile_per_minute",
    "Bowel sounds per minute, 9th decile": "ninth_decile_per_minute",
    "Bowel sounds per minute, mean": "mean_per_minute",
    "Bowel sounds per minute, median": "median_per_minute",
    "Bowel sounds per minute, minimum": "minimum_per_minute",
    "Bowel sounds per minute, standard deviation": "deviation_per_minute",
    "Bowel sounds per minute, total": "total_sound_index",
    "Recording length, hours:minutes:seconds": "length",
}

model_mock = {
    'bowell_sounds_number': 0.01,
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


async def send_websocket_message(group_name: str, message: dict):
    """Sends websocket message via channel_layer"""

    channel_layer = get_channel_layer()
    logger.debug(f"trying to send message via channel_layer.group_send")
    try:
        await channel_layer.group_send(group_name, message)
        logger.debug(f"sent message via channel_layer")
    except Exception as e:
        logger.warning("Failed to send a message via channel_layer.group_send")
        logger.warning(e)


class BaseTask(Task):
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        recording_id, _, user_id = args
        ex = Examination.objects.filter(recording__id=recording_id)
        ex.update(status=Examination.Statuses.processing_succeeded)
        serialized = ExaminationSerializer(ex.first()).data

        asyncio.run(
            send_websocket_message(
                group_name=f"user-{user_id}",
                message={
                    "type": "update_examination",
                    "message": f"Analysis of recording {recording_id} completed!",
                    "payload": serialized
                }
            )
        )
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        recording_id, _, user_id = args
        # set status to processing_failed
        ex = Examination.objects.filter(recording__id=recording_id)
        ex.update(status=Examination.Statuses.processing_failed)
        serialized = ExaminationSerializer(ex.first()).data
        # send ws message that analysis failed
        asyncio.run(
            send_websocket_message(
                group_name=f"user-{user_id}",
                message={
                    "type": "update_examination",
                    "message": f"Analysis of recording {recording_id} failed!",
                    "payload": serialized
                }
            )
        )
        return super().on_failure(exc, task_id, args, kwargs, einfo)


@app.task(bind=True, base=BaseTask)
def process_recording(self, recording_id: int, file_path: str, user_id: int):
    logger.info(f"started processing of Recording ID={recording_id}")

    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#id7
    req = self.request  # task details

    # attach task_id to examination
    examination = Examination.objects.get(recording__id=recording_id)
    examination.analysis_id = req.id
    examination.status = Examination.Statuses.file_processing
    examination.save(update_fields=['analysis_id', 'status'])

    asyncio.run(
        send_websocket_message(
            group_name=f"user-{user_id}",
            message={
                "type": "notify",
                "message": f"Started processing of recording with id: {recording_id}"
            }
        )
    )

    if settings.CELERY_USE_MOCK_MODEL:
        response = call_mock()
        logger.info("Received response from ml model")

        asyncio.run(
            send_websocket_message(
                group_name=f"user-{user_id}",
                message={
                    "type": "notify",
                    "message": "Received response from model"
                }
            )
        )

        data = {
            **response["statistics"]["Main results"],
            "probability_plot": response["frames"]
        }
    else:
        data = call_model(file_path, user_id)

    Recording.objects.filter(id=recording_id).update(**data)

    logger.info(f"Successfully updated recording {recording_id}")
    return RecordingAfterAnalysisSerializer(Recording.objects.get(id=recording_id)).data


def call_model(file_path: str, user_id: int):
    url = f"{settings.CELERY_MODEL_URL}/inference"
    print(f"FILE path: {file_path}")
    files = [
        ('file', open(file_path, 'rb'))
    ]
    logger.info("Sending request to ml model")

    response = requests.request("POST", url, files=files)

    logger.info(f"Received response from ml model, status {response.status_code}")
    asyncio.run(
        send_websocket_message(
            group_name=f"user-{user_id}",
            message={
                "type": "notify",
                "message": "Received response from model"
            }
        )
    )

    data = response.json()
    raw_data = data["frames"]
    stats = data["statistics"]["Main results"]

    results = {v: stats[k] for k, v in mapper.items()}
    results["probability_plot"] = raw_data
    return results


def call_mock():
    # mocked frames used for probability plot
    frames = [{"start": round(i / 1000, 2), "probability": random.random()} for i in range(0, 1000, 1)]
    # shape of actual model response
    results = {"code": 200, "error": "", "frames": frames, "statistics": {"Main results": model_mock}}
    return results
