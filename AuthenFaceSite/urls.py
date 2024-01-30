from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<int:id>/', views.user, name='user'), 
    path('user-images/', views.user_image_list),
    path('user-images/<int:id>/', views.user_image, name='user-image'), 
]
