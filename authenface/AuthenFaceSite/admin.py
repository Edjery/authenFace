from django.contrib import admin
from .models import AuthenFaceUser, Snapshots, UserImage, Websites

# Register your models here.
admin.site.register(AuthenFaceUser)
admin.site.register(UserImage)
admin.site.register(Snapshots)
admin.site.register(Websites)