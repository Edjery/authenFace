from django.contrib import admin
from .models import AuthenFaceUser, Snapshot, Website

@admin.register(AuthenFaceUser)
class AuthenFaceUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password', 'image')

@admin.register(Snapshot)
class SnapshotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'image', 'created_at')

@admin.register(Website)
class WebsitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'account_name', 'user', 'created_at')
