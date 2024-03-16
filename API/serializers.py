from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password

from .models import AuthenFaceUser, Snapshot, Website, DummyUser

from rest_framework import serializers

class AuthenFaceUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
     
    class Meta:
        model = AuthenFaceUser
        fields = ['id', 'name', 'email', 'image', 'password',]

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ['id', 'name', 'image', 'user', 'created_at']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'url', 'account_name', 'user', 'created_at']

class DummyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyUser
        fields = ['id', 'email', 'password']