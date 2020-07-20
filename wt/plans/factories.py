import factory
from faker import Factory

from wt.plans.models import Plan

faker = Factory.create()


class PlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = Plan