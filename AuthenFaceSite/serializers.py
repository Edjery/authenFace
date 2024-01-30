from rest_framework import serializers
from .models import AuthenFaceUser, Snapshot, UserImage, Website

class AuthenFaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenFaceUser
        fields = ['id', 'email']

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'name']

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ['id', 'user', 'createdAt']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'url', 'accountName', 'user', 'createdAt']