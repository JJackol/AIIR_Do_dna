from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:calculation_name>/', views.track_progress, name='tracker'),
    path('demo/<str:calculation_name>/<str:message>', views.websocket_sending_message_demo, name='demo'),
]
