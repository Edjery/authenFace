from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.userList),
    path('users/<int:id>/', views.user, name='user'), 
]
