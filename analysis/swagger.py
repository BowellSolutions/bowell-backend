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

author: Adam Lisichin

description: File consists of serializers definition used only for swagger documentation.
"""
from rest_framework import serializers
from celery.states import PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
from recordings.serializers import RecordingAfterAnalysisSerializer


class InferenceResponseSerializer(serializers.Serializer):
    """Serializer used for swagger documentation.
    Return type of response at GET /api/examinations/<id>/inference/"""
    task_id = serializers.CharField(max_length=36)
    status = serializers.ChoiceField(choices=(
        PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
    ))
    # optional result
    result = RecordingAfterAnalysisSerializer(required=False)
