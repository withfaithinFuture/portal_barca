# users/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/likes/(?P<content_type>\w+)/(?P<content_id>\d+)/$', consumers.LikeConsumer.as_asgi()),
]