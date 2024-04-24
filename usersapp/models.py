from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']