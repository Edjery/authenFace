from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='camera'),
    path('video_feed', views.video_feed, name='video_feed'),
]