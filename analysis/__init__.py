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

authors: Adam Lisichin, Gustaw Daczkowski

description: Analysis application with Celery app - entrypoint for Celery worker, Celery task and utility methods,
Dashboard websocket consumer, websocket routing.

structure:
    - migrations/                   # migrations package
    - tests/                        # unit tests package
        - test_mocked_model.py      # celery tasks unit tests
    - __init__.py                   # exports Celery app so it is available within the module
    - admin.py                      # file for potential registration of models and model admins
    - apps.py                       # analysis app config
    - celery.py                     # Celery app setup and configuration
    - consumers.py                  # Dashboard Consumer which handles websocket messages
    - models.py                     # file for potential model definitions
    - routing.py                    # mapping websocket consumer to websocket route
    - swagger.py                    # auxiliary serializers used in Swagger documentation
    - tasks.py                      # Celery tasks definition and helper functions
    - views.py                      # file for potential view definitions
"""
from .celery import app as celery_app

__all__ = ('celery_app',)
