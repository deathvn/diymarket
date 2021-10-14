from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Create your models here.

class Order(models.Model):
    """Model representing an order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(
        max_length=1,
        choices=settings.TYPE_CHOICE,
        null=True,
        help_text='Buy or Sell order',
    )
    location = models.CharField(
        max_length=1,
        choices=settings.LOCATION_CHOICE,
        default='3',
        help_text='Enter the location of order'
    )
    item_id = models.CharField(max_length=100, help_text='Enter the UniqueName of item')
    price = models.PositiveIntegerField(default=0, help_text='Price of item')
    amount = models.PositiveIntegerField(default=0, help_text='Number of item')
    username = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class OrderMatching(models.Model):
    """Model representing an order matching"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0, help_text='Number of item')
    username = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=1,
        choices=settings.STATUS_CHOICE,
        default='0',
        help_text='Status of order',
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.order}'