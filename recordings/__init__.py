"""
authors: Wojciech Nowicki, Hubert Decyusz

description: Package contains structure and functionality of Recording model including:
    - model definition
    - viewset
    - serializers
    - api endpoints
    - unit tests

structure:
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - __init__.py
        - test_api_views.py                 # unit tests of endpoints, views, serializers within recordings app
    - __init__.py
    - admin.py                              # registration of Recording model in admin interface
    - apps.py                               # recordings app config
    - models.py                             # definition of Recording model
    - serializers.py                        # model serializers (CRUD, data representation and validation)
    - urls.py                               # mapping viewset to endpoint
    - views.py
"""
