## File Structure

```
.github/                                    
    - workflows/                            # definitions of Github Action workflows
        - backend-ci.yaml                   # CI/CD workflow
        - build_agents.yml                  # custom build agents
analysis/
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - test_mocked_model                 # celery task unit tests
    - __init__.py                           # exports Celery app so it is available within the module
    - admin.py                              # file for potential registration of models and model admins [EMPTY]
    - apps.py                               # analysis app config
    - celery.py                             # Celery app setup and configuration
    - consumers.py                          # Dashboard Consumer which handles websocket messages
    - models.py                             # file for potential model definitions [EMPTY]
    - routing.py                            # mapping of consumer to websocket route
    - swagger.py                            # auxiliary serializers used in Swagger documentation
    - tasks.py                              # Celery task definition and helper functions
    - views.py                              # file for potential view definitions [EMPTY]
core/
    - management/
        - commands/                         # package for custom commands
            - __init__.py
            - wait_for_db.py                # defines wait_for_db command which can be run with manage.py
        - __init__.py
    - settings/
        - __init__.py
        - base.py                           # base settings, which are extented by other settings files
        - dev.py                            # development settings
        - heroku.py                         # settings for deployment to Heroku
        - prod.py                           # production settings - deployment to Kubernetes cluster
    - __init__.py
    - asgi.py                               # asgi application - entrypoint to Daphne server, contains setup for http and ws protocols
    - urls.py                               # top-level definition of routing, includes admin and routes from applications
    - wsgi.py                               # wsgi application - not used
examinations/
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - __init__.py
        - test_api_views.py                 # unit tests of endpoints, views, serializers within examinations app
    - __init__.py
    - admin.py                              # registration of Examination model and its admin with custom form in admin interface
    - apps.py                               # examinations app config
    - models.py                             # definition of Examination model
    - serializers.py                        # model serializers (CRUD, data representation and validation)
    - swagger.py                            # auxiliary serializers used in Swagger documentation
    - urls.py                               # mapping examination viewset to endpoints
    - views.py                              # examination viewset with extra action (CRUD + starting/checking inference)
media/                                      # storage for saved recordings
recordings/
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
    - views.py                              # recordings viewset (CRUD)
scripts/                                    
    - entrypoint-dev.sh                     # development Dockerfile entrypoint
    - entrypoint-prod.sh                    # production Dockerfile entrypoint
users/
    - migrations/                           # migrations package
    - tests/                                # unit tests package
        - __init__.py
        - test_api_views.py                 # unit tests of endpoints, views, serializers within users app
    - __init__.py
    - admin.py                              # registration of custom User, UserAdmin with custom forms in admin interface
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
.coveragerc                                 # coverage package config
.dockerignore
.editorconfig                               # uniform code formatting
.gitignore
docker-compose.yml                          # docker-compose for local development, contains definitions of services and volumes
Dockerfile                                  # backend container dockerfile
Dockerfile.Celery                           # celery container dockerfile
Dockerfile.prod                             # production ready dockerfile
manage.py                                   # Django CLI
mypy.ini                                    # mypy config
Procfile                                    # Heroku entrypoint file
README.md
requirements.txt                            # dependencies
runtime.txt                                 # contains Python version used by Heroku
```
