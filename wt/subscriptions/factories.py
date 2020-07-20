import factory
from faker import Factory

from django.contrib.auth.models import User

from wt.plans.factories import PlanFactory
from wt.subscriptions.models import ATTSubscription, SprintSubscription

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')


class ATTSubscriptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ATTSubscription

    # user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)


class SprintSubscriptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = SprintSubscription

    # user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)
