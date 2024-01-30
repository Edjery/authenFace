from django.db import models

class DummyUser (models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    passwoord = models.CharField(max_length=50)
