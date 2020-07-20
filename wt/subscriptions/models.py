from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from model_utils import Choices

from wt.plans.models import Plan


class Device(models.Model):
    # Owning user
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    device_id = models.CharField(max_length=20, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    phone_model = models.CharField(max_length=128, blank=True, default='')


class BaseSubscriptions(models.Model):

    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.PROTECT)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.PROTECT)

    effective_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ATTSubscription(BaseSubscriptions):
    """Represents a subscription with AT&T for a device"""

    ONE_KILOBYTE_PRICE = Decimal('0.001')
    ONE_SECOND_PRICE = Decimal('0.001')

    STATUS = Choices(
        ('new', 'New'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    )

    status = models.CharField(max_length=10, choices=STATUS, default=STATUS.new)
    network_type = models.CharField(max_length=5, blank=True, default='')


class SprintSubscription(BaseSubscriptions):
    """Represents a subscription with Sprint for a device"""

    ONE_KILOBYTE_PRICE = Decimal('0.0015')
    ONE_SECOND_PRICE = Decimal('0.0015')

    STATUS = Choices(
        ('new', 'New'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    )

    status = models.CharField(max_length=10, choices=STATUS, default=STATUS.new)
    sprint_id = models.CharField(max_length=16, blank=True)
