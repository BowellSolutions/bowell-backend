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

description: Package contains structure and functionality of Examination model including:
    - model definition
    - viewset
    - serializers
    - api endpoints
    - unit tests

structure:
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - __init__.py
        - test_api_views.py                 # unit tests of endpoints, views, serializers within examinations app
    - __init__.py
    - admin.py                              # registration of Examination model and its admin with custom form
                                            # in admin interface
    - apps.py                               # examinations app config
    - models.py                             # definition of Examination model
    - serializers.py                        # model serializers (CRUD, data representation and validation)
    - swagger.py                            # auxiliary serializers used in Swagger documentation
    - urls.py                               # mapping examination viewset to endpoints
    - views.py                              # examination viewset with extra action (CRUD + starting/checking inference)
"""
