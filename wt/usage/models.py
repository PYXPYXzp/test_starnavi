from django.db import models

from wt.subscriptions.models import ATTSubscription
from wt.subscriptions.models import SprintSubscription


class BaseUsageRecord(models.Model):
    """Base model for usage record"""
    att_subscription = models.ForeignKey(ATTSubscription, null=True, blank=True, on_delete=models.PROTECT)
    sprint_subscription = models.ForeignKey(SprintSubscription, null=True, blank=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class DataUsageRecord(BaseUsageRecord):
    """Raw data usage record for a subscription"""
    kilobytes_used = models.IntegerField(blank=True, null=True)


class VoiceUsageRecord(BaseUsageRecord):
    """Raw voice usage record for a subscription"""
    seconds_used = models.IntegerField(blank=True, null=True)


class BaseAggregateData(models.Model):
    """Base model for usage aggregated data"""
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    aggregated_price = models.DecimalField(decimal_places=2, max_digits=5, default=0)

    class Meta:
        abstract = True


class AggregateDataUsage(BaseAggregateData):
    """Aggregated data usage"""
    data_records = models.ManyToManyField(DataUsageRecord)
    aggregated_kilobytes_used = models.IntegerField(blank=True, null=True)


class AggregateVoiceUsage(BaseAggregateData):
    """Aggregated voice usage"""
    voice_records = models.ManyToManyField(VoiceUsageRecord)
    aggregated_seconds_used = models.IntegerField(blank=True, null=True)
