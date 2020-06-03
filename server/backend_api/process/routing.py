from django.urls import re_path

from . import consumers

# Adresy URL pod którymi dostępne są websocketowe kanały
websocket_urlpatterns = [
    re_path(r'get_progress/(?P<tracker_name>\w+)/$', consumers.ProgressConsumer),
]