# Python imports
from typing import Dict, Any
import logging
import datetime
# django/rest_framwork imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# app level imports
from .managers import UserManager


class Wallet(AbstractBaseUser):
    """
    User model represents the user data in the database.
    """

    mobile = models.BigIntegerField(
        unique=True,
        null=True,)
    is_staff = models.BooleanField(
        default=False,
    )
    password = models.CharField(max_length=256, blank=True)
    name = models.CharField(max_length=64, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "mobile"

    class Meta:
        db_table = "wallet"

    def __str__(self):
        return str(self.mobile)

    def modify(self, payload: Dict[str, Any]):
        """
        This will update license object
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()


class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet',on_delete=models.PROTECT,related_name='transactions')
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=15,null=False)
    balance = models.BigIntegerField(default=0)
    

