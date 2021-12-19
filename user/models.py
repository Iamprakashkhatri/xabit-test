import binascii
import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """
    model for user informations
    """

    username=models.CharField(primary_key=True,max_length=200,default=uuid.uuid4)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    profile_picture = models.URLField(help_text="Photo of user", default=None, null=True, blank=True)
    is_mobile_app_user=models.BooleanField(default=True)

    # USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")

    def __str__(self):
        return self.first_name


class Roll(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class RollList(models.Model):
    class Meta:
        unique_together = (('roll', 'user'),)

    roll= models.ForeignKey(Roll, on_delete=models.CASCADE, related_name="roll_lists")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="roll_list")

    def __str__(self):
        return f"{self.roll.name}-{self.user.first_name}"



        
