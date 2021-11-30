import os
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from examinations.models import Examination
from recordings.models import Recording
from recordings.serializers import RecordingBeforeAnalysisSerializer
from users.utils import get_tokens_for_user

TEST_FILES_DIR = os.path.join(settings.BASE_DIR.parent, 'test_files')

User = get_user_model()


class TestRecordingsAPIViews(TestCase):
    def setUp(self):
        # recreate data on each run
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls):
        # create data before running any tests
        cls.user1 = User.objects.create(username="test1", password="test1")
        cls.exam1 = Examination.objects.create(doctor=cls.user1, date=timezone.now())

        rec = SimpleUploadedFile("file.wav", b"file_content", content_type="audio/wav")
        cls.recording1 = Recording.objects.create(
            file=rec,
            name='test.txt'
        )

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

    def test_list_recordings(self):
        self._require_jwt_cookies(user=self.user1)
        response = self.client.get("/api/recordings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # to do test response with serialized data

    def test_list_recordings_empty(self):
        pass

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

    def test_create_recording_empty(self):
        pass

    def test_create_recording_without_examination(self):
        pass

    def test_create_recording_already_assigned_to_examination(self):
        pass

    def test_create_recording_name_missing(self):
        pass

    def test_create_recording_file_missing(self):
        pass

    # to do more
