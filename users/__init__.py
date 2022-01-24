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
