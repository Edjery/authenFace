from rest_framework import serializers
from .models import AuthenFaceUser, Snapshot, UserImage, Website

class AuthenFaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenFaceUser
        fields = ['id', 'email', 'password']

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'name', 'user']

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ['id', 'name', 'user', 'created_at']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'url', 'account_name', 'user', 'created_at']