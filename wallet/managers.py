# django imports
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        """
        Creates and saves a User with the given mobile number and password.
        AbstractBaseUser requires
        """
        if not mobile:
            raise ValueError("Users must have a mobile num")

        user = self.model(mobile= mobile,**extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given mobile number and password.
        """
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
