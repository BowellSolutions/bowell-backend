from django.urls import re_path

from .consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'^ws/users/(?P<user_code>[^/]+)/$', DashboardConsumer.as_asgi()),
]
