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

description: File registers Examination model and its model admin with custom model form in admin interface.
"""
from django import forms
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

from analysis.tasks import process_recording
from .models import Examination

User = get_user_model()


class ExaminationModelForm(forms.ModelForm):
    """Examination form with filtered doctor and patient choice fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filter doctors and patients
        self.fields['doctor'].queryset = User.objects.doctors()
        self.fields['patient'].queryset = User.objects.patients()
        self.fields['analysis_id'].help_text = "Celery task UUID"

    class Meta:
        model = Examination
        fields = "__all__"


class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'patient', 'doctor', 'date')
    list_filter = ('status', 'date')
    form = ExaminationModelForm
    change_form_template = "examinations/admin/examination_change.html"

    def response_change(self, request: HttpRequest, obj: Examination) -> HttpResponse:
        # handle custom analyze button
        if obj.recording is not None and "run_analysis" in request.POST:
            # run celery task
            task = process_recording.delay(obj.recording.id, obj.recording.file.path, request.user.id)
            message = f"Started analysis of {obj.recording}. Task ID {task.id}"
            # refresh page and display success message above
            self.message_user(request, message, messages.SUCCESS)
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Examination, ExaminationAdmin)
