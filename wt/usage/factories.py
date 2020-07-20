import factory
from faker import Factory

from wt.usage.models import DataUsageRecord, VoiceUsageRecord
from wt.subscriptions.factories import ATTSubscriptionFactory


faker = Factory.create()


class DataUsageRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = DataUsageRecord

    att_subscription = factory.SubFactory(ATTSubscriptionFactory)


class VoiceUsageRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = VoiceUsageRecord

    att_subscription = factory.SubFactory(ATTSubscriptionFactory)
