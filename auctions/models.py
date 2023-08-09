from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listings(models.Model):
    item_title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
