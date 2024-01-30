from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersAPI.manage_all),
    path('users/<int:id>/', views.UsersAPI.manage), 
    path('user-images/', views.UserImagesAPI.manage_all),
    path('user-images/<int:id>/', views.UserImagesAPI.manage), 
    path('snapshots/', views.SnapshotsAPI.manage_all),
    path('snapshots/<int:id>/', views.SnapshotsAPI.manage), 
]
