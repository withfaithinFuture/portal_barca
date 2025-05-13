from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('auth/', auth_view, name='auth'),
]

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/likes/(?P<content_type>\w+)/(?P<content_id>\d+)/$', consumers.LikeConsumer.as_asgi()),
]