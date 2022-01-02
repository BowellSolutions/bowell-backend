"""
author: Wojciech Nowicki, Hubert Decyusz
description: File contains tests used for
recordings app testing.
"""

import os
import shutil
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from examinations.models import Examination
from recordings.models import Recording
from recordings.serializers import RecordingBeforeAnalysisSerializer, RecordingAfterAnalysisSerializer
from users.utils import get_tokens_for_user
from datetime import timedelta

TEST_FILES_DIR = os.path.join(settings.BASE_DIR.parent, 'test_files')

User = get_user_model()


class TestRecordingsAPIViews(TestCase):
    def setUp(self):
        # recreate data on each run
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls):
        # create data before running any tests
        cls.user1 = User.objects.create_user(email="test43@gmail.com", password="test1",
                                             first_name="", last_name="", type=User.Types.PATIENT)
        cls.exam1 = Examination.objects.create(doctor=cls.user1, date=timezone.now())

        # use test_files directory for writing files in tests
        Path('test_files').mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # remove test_files directory after tests
        if os.path.exists(TEST_FILES_DIR):
            shutil.rmtree(TEST_FILES_DIR)

    def _require_jwt_cookies(self, user) -> None:
        """Client will attach valid JWT Cookies - to be rewritten as method decorator"""
        access, refresh = get_tokens_for_user(user=user)
        self.client.cookies.load({
            'access': access,
            'refresh': refresh,
        })

    def test_viewset_user_not_authorized(self):
        r_get = self.client.get("/api/recordings/")
        self.assertEqual(r_get.status_code, status.HTTP_401_UNAUTHORIZED)

        r_post = self.client.post("/api/recordings/", {})
        self.assertEqual(r_post.status_code, status.HTTP_401_UNAUTHORIZED)

        r_put = self.client.put("/api/recordings/1/")
        self.assertEqual(r_put.status_code, status.HTTP_401_UNAUTHORIZED)

        r_patch = self.client.patch("/api/recordings/1/")
        self.assertEqual(r_patch.status_code, status.HTTP_401_UNAUTHORIZED)

        r_delete = self.client.delete("/api/recordings/1/")
        self.assertEqual(r_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recording(self):
        self._require_jwt_cookies(self.user1)

        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'xd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        self.assertEqual(response.json(), RecordingBeforeAnalysisSerializer(file).data)

    def test_create_recording_with_uploader(self):
        self._require_jwt_cookies(self.user1)

        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'xd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'uploader': self.user1.id,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        self.assertEqual(response.json(), RecordingBeforeAnalysisSerializer(file).data)

    def test_create_recording_empty(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recording_without_examination(self):
        self._require_jwt_cookies(self.user1)

        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'xd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recording_already_assigned_to_examination(self):
        self._require_jwt_cookies(self.user1)

        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'esd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open(f'{TEST_FILES_DIR}/test1.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recording_name_missing(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recording_file_missing(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_recordings(self):
        self._require_jwt_cookies(user=self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'xd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exam2 = Examination.objects.create(doctor=self.user1, date=timezone.now() + timedelta(days=1))

        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'xd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': exam2.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/recordings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_current_recordings(self):
        self._require_jwt_cookies(user=self.user1)
        response = self.client.get("/api/recordings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_recording_file_one_attribute(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        bowell_sounds = 25
        response = self.client.patch(f"/api/recordings/{file_id}/", {
            'bowell_sounds_number': bowell_sounds
        }
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        file = Recording.objects.get(name="fart.wav")
        self.assertEqual(response.json(), RecordingAfterAnalysisSerializer(file).data)

    def test_update_recording_file_two_attributes(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        bowell_sounds = 25
        deviation_per_minute = 20.5
        response = self.client.patch(f"/api/recordings/{file_id}/", {
            'bowell_sounds_number': bowell_sounds,
            'deviation_per_minute': deviation_per_minute
        }
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        file = Recording.objects.get(name="fart.wav")
        self.assertEqual(response.json(), RecordingAfterAnalysisSerializer(file).data)

    def test_update_recording_file_multiple_attributes(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        response = self.client.patch(f"/api/recordings/{file_id}/", {
            "length": '20',
            "bowell_sounds_number": 25,
            "bowell_sounds_per_minute": 5.6,
            "mean_per_minute": 50,
            "deviation_per_minute": 9999,
            "median_per_minute": 12,
            "first_quartile_per_minute": 5.0,
            "third_quartile_per_minute": 10,
            "first_decile_per_minute": 62.8,
            "ninth_decile_per_minute": 11,
            "minimum_per_minute": 65,
            "maximum_per_minute": 35,
            "repetition_within_50ms": 23,
            "repetition_within_100ms": 106,
            "repetition_within_200ms": 232323,
            "containing_30s_periods_percentage": 80,
        }
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_recording_file_wrong_attribute_type(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        bowell_sounds = 'abcd'

        response = self.client.patch(f"/api/recordings/{file_id}/", {
            'bowell_sounds_number': bowell_sounds,
        }
                                     )
        file = Recording.objects.get(name="fart.wav")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recording_file_one_wrong_attribute_type(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        bowell_sounds = 25
        deviation_per_minute = 'abcd'
        response = self.client.patch(f"/api/recordings/{file_id}/", {
            'bowell_sounds_number': bowell_sounds,
            'deviation_per_minute': deviation_per_minute
        }
                                     )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recording_file_wrong_attribute_chosen(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        name = 'abc'
        response = self.client.patch(f"/api/recordings/{file_id}/", {
            'name': name
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recording = Recording.objects.get(name="fart.wav")
        self.assertNotEqual(recording.name, name)

    def test_delete_recording(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        response = self.client.delete(f"/api/recordings/{file_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_the_same_recording_twice(self):
        self._require_jwt_cookies(self.user1)
        with open(f'{TEST_FILES_DIR}/test.wav', 'wb+') as fp:
            fp.write(b'abcd')
            fp.seek(0)
            response = self.client.post("/api/recordings/", {
                'file': fp,
                'name': 'fart.wav',
                'examination': self.exam1.id
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file = Recording.objects.get(name="fart.wav")
        file_id = file.id
        response = self.client.delete(f"/api/recordings/{file_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(f"/api/recordings/{file_id}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Recording was not assigned to any examination.'})

    def test_delete_non_existing_recording(self):
        self._require_jwt_cookies(self.user1)
        wrong_id = 'abcd'
        response = self.client.delete(f"/api/recordings/{wrong_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
