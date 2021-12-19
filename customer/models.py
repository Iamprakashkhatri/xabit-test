import binascii
import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin
from common.models import TimeStampedModel
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from user.models import User

class CustomerTier(models.Model):
    CustomerType = (
        ("general", "general"),
        ("regular", "regular"),
        ("staff", "staff"),
        ("ncell","ncell"),
    	("vip","vip"),
    )
    name = models.CharField(max_length=31, choices=CustomerType, default="general")
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)
    discount_cap = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return self.name

class Customer(TimeStampedModel):
    """
    model for customer informations
    """
    Gender_Choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Non-binary", "Non-binary"),
    )

    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    gender = models.CharField(max_length=50,choices=Gender_Choices,default="Male")
    birth_date = models.DateField(blank=True, null=True)
    customer_tier = models.ForeignKey(CustomerTier, on_delete=models.CASCADE, related_name="customer",null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customeruser")

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return f'{self.user.first_name}'

    # @property
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"

# class MyOwnToken(models.Model):
#     class Meta:
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")

#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     # user = models.OneToOneField(
#     #     User, related_name='user_auth_token',
#     #     on_delete=models.CASCADE, verbose_name="Customers"
#     # )
#     customer = models.OneToOneField(
#         Customer, related_name='customer_auth_token',
#         on_delete=models.CASCADE,verbose_name="Customers"
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(MyOwnToken, self).save(*args, **kwargs)

#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key

#     @property
#     def is_authenticated(self):
#         """
#         Always return True. This is a way to tell if the user has been
#         authenticated in templates.
#         """
#         return True