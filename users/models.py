from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    organization = models.ForeignKey('spaces.Organization', on_delete=models.CASCADE,
                                     related_name='users', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username