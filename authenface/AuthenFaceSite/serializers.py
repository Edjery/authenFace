from rest_framework import serializers

from .models import AuthenFaceUser, Snapshot, UserImage, Website

class AuthenFaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenFaceUser
        fileds = ['id', 'email']

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fileds = ['id', 'name']

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fileds = ['id', 'user', 'createdAt']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fileds = ['id', 'name', 'url', 'accountName', 'user', 'createdAt']