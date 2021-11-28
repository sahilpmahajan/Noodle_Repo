from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import UserManager


# CUSTOM USER MODEL
class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    roll_number = models.CharField(unique=True, blank=False,default=0, max_length=10)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()