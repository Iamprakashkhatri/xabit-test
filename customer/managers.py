from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # email = self.normalize_email(email)
        user = self.model(first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(first_name, password, **extra_fields)


# class UserManager(BaseUserManager):

#     def create_user(self, first_name, last_name, email, phone_number,password, gender, birth_date,profile_picture,is_active=True,is_staff=False):
#         if not first_name:
#             raise ValueError("User must have an first_name")
#         if not last_name:
#             raise ValueError("User must have a last name")
#         if not password:
#             raise ValueError("User must have a password")
#         if not phone_number:
#             raise ValueError("User must have a phone_number")

#         user = self.model()

#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.set_password(password)  # change password to hash
#         user.phone_number = phone_number
#         user.gender = gender
#         user.birth_date = birth_date
#         user.is_active = is_active
#         user.profile_picture = profile_picture
#         user.is_staff = is_staff
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, first_name,last_name,email, phone_number,password=None):
#         user = self.create_user(
#             first_name,
#             last_name,
#             email,
#             phone_number,
#             password=password,
#             is_staff=True,
#         )
#         return user

#     def create_superuser(self,first_name,last_name, email, phone_number,password=None):
#         user = self.create_user(
#             first_name,
#             last_name,
#             email,
#             phone_number,
#             password=password,
#             is_staff=True,
#             is_admin=True,
#         )
#         return user