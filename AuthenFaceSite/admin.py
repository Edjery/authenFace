from django.contrib import admin
from .models import AuthenFaceUser, Snapshot, UserImage, Website

@admin.register(AuthenFaceUser)
class AuthenFaceUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    
@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
@admin.register(Snapshot)
class SnapshotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'createdAt')
@admin.register(Website)
class WebsitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'accountName', 'user', 'createdAt')
