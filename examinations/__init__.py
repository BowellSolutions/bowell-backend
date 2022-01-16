"""
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
