"""
authors: Adam Lisichin, Hubert Decyusz

description: Users app provides custom User model with its object manager, AuthorizationHeaderMiddleware,
CurrentUserOrAdminPermission, User serializers, UserViewSet and GetCurrentUser views, token and cookie utility functions

structure:
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - __init__.py
        - test_api_views.py                 # unit tests of endpoints, views, serializers within users app
    - __init__.py
    - admin.py                              # registration of custom User, UserAdmin with custom forms
                                            # in admin interface
    - apps.py                               # users app config
    - middleware.py                         # middleware which injects access cookie into request headers
    - models.py                             # custom User and its object manager
    - permissions.py                        # additional permissions
    - serializers.py                        # model serializers (CRUD, data representation and validation)
    - swagger.py                            # auxiliary serializers used in Swagger documentation
    - urls.py                               # mapping views to endpoints
    - utils.py                              # utility functions for retrieving tokens, cookie parameters
    - validators.py                         # validators used in User model
    - views.py                              # auth and user related views, User viewset (CRUD)
"""
