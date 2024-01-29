from django.db import models

class AuthenFaceUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)

class Snapshots(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)

class Websites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    accountName = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)