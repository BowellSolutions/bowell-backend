"""
Copyright (c) 2022 Adam Lisichin, Hubert Decyusz, Wojciech Nowicki, Gustaw Daczkowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

author: Hubert Decyusz

description: File contains tests used for examinations app testing.
"""
import os
import shutil
from datetime import timedelta
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
from users.utils import get_tokens_for_user

TEST_FILES_DIR = os.path.join(settings.BASE_DIR.parent, 'test_files')

User = get_user_model()


class TestExaminationsAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            email="test1@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        cls.user2 = User.objects.create_user(
            email="test3@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
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
        r_get = self.client.get("/api/examinations/")
        self.assertEqual(r_get.status_code, status.HTTP_401_UNAUTHORIZED)

        r_post = self.client.post("/api/examinations/", {})
        self.assertEqual(r_post.status_code, status.HTTP_401_UNAUTHORIZED)

        r_put = self.client.put("/api/examinations/1/")
        self.assertEqual(r_put.status_code, status.HTTP_401_UNAUTHORIZED)

        r_patch = self.client.patch("/api/examinations/1/")
        self.assertEqual(r_patch.status_code, status.HTTP_401_UNAUTHORIZED)

        r_delete = self.client.delete("/api/examinations/1/")
        self.assertEqual(r_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_examinations(self):
        self._require_jwt_cookies(user=self.user1)
        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/examinations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_current_examinations(self):
        self._require_jwt_cookies(user=self.user1)
        response = self.client.get("/api/examinations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [])

    def test_create_examination(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_examination_empty(self):
        self._require_jwt_cookies(self.user1)
        response = self.client.post("/api/examinations/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_examination_without_doctor(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'date': timezone.now()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_examination_without_date(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'doctor': self.user1.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_examination_with_patient(self):
        self._require_jwt_cookies(self.user1)
        user2 = User.objects.create_user(
            email="test2@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        response = self.client.post("/api/examinations/", {
            'patient': user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_examination_with_recording(self):
        self._require_jwt_cookies(self.user1)
        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1),
            'recording': self.recording1.id  # unnecessary attribute
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(id=response.json()['id'])
        self.assertNotEqual(examination.recording, self.recording1)

    def test_create_examination_with_wrong_date(self):
        self._require_jwt_cookies(self.user1)
        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'recording': self.recording1.id,
            'doctor': self.user1.id,
            'date': timezone.now()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_examination_one_attribute(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'overview': 'abc'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_examination_multiple_attributes(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'overview': 'abc',
            'height_cm': '180',
            'symptoms': 'abcd'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_examination_attribute_wrong_type(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'height_cm': 180,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_examination_multiple_attributes_one_wrong_type(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'overview': 'abc',
            'height_cm': 180,
            'symptoms': 'abcd'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_examination_height_out_of_scope(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'height_cm': 18000,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_examination_mass_out_of_scope(self):
        self._require_jwt_cookies(self.user1)

        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1)

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(doctor=self.user1)
        examination_id = examination.id
        response = self.client.patch(f"/api/examinations/{examination_id}/", {
            'mass_kg': 1000,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_examination_with_already_assigned_recording(self):
        self._require_jwt_cookies(self.user1)
        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(id=response.json()['id'])
        response = self.client.patch(f"/api/examinations/{examination.id}/", {"recording": self.recording1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post("/api/examinations/", {
            'patient': self.user2.id,
            'doctor': self.user1.id,
            'date': timezone.now() + timedelta(days=1),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        examination = Examination.objects.get(id=response.json()['id'])
        response = self.client.patch(f"/api/examinations/{examination.id}/", {"recording": self.recording1.id})
        self.assertEqual(response.json(),
                         {'detail': 'Another recording has already been assigned to chosen examination.'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_is_doctor(self):
        user1 = User.objects.create_user(
            email="test12@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        self._require_jwt_cookies(user1)
        response = self.client.get("/api/statistics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_not_doctor(self):
        user1 = User.objects.create_user(
            email="test13@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        self._require_jwt_cookies(user1)
        response = self.client.get("/api/statistics/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pending_examinations(self):
        user1 = User.objects.create_user(
            email="test14@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        user2 = User.objects.create_user(
            email="test21@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        user3 = User.objects.create_user(
            email="test31@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        user4 = User.objects.create_user(
            email="test41@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        user5 = User.objects.create_user(
            email="test51@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        user6 = User.objects.create_user(
            email="test61@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        user7 = User.objects.create_user(
            email="test71@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        Examination.objects.create(
            doctor=user1, patient=user2, date=timezone.now() + timedelta(days=2), status="processing_succeeded"
        )
        Examination.objects.create(
            doctor=user1, patient=user3, date=timezone.now() + timedelta(days=12), status="scheduled"
        )
        Examination.objects.create(
            doctor=user1, patient=user4, date=timezone.now() + timedelta(days=8), status="processing_succeeded"
        )
        Examination.objects.create(
            doctor=user1, patient=user5, date=timezone.now() + timedelta(days=4), status="scheduled"
        )
        Examination.objects.create(
            doctor=user1, patient=user6, date=timezone.now() + timedelta(days=11), status="file_processing"
        )
        Examination.objects.create(
            doctor=user1, patient=user7, date=timezone.now() + timedelta(days=3), status="file_uploaded"
        )
        Examination.objects.create(
            doctor=user1, patient=user5, date=timezone.now() + timedelta(days=2), status="processing_failed"
        )
        Examination.objects.create(
            doctor=user1, patient=user4, date=timezone.now() + timedelta(days=4), status="scheduled"
        )
        self._require_jwt_cookies(user1)
        response = self.client.get("/api/statistics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'examination_count': 8,
                'patients_related_count': 6,
                'examinations_scheduled_count': 6,
                'examinations_next_week_count': 4
            }
        )
