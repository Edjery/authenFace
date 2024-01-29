from django.db import models

class AuthenFaceUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.email

class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Snapshots(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Websites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    accountName = models.CharField(max_length=50)
    userId = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name