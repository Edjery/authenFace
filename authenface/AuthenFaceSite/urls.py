from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = 'AuthenFace Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('users/', views.userList),
]
