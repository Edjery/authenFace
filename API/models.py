from django.db import models

class AuthenFaceUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    userImageName = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.email

# class UserImage(models.Model):
#     name = models.CharField(max_length=50)
#     user = models.OneToOneField(AuthenFaceUser, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.name

class Snapshot(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(AuthenFaceUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Website(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    account_name = models.CharField(max_length=50)
    user = models.ForeignKey(AuthenFaceUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
class DummyUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.email