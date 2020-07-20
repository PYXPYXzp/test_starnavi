from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from wt.subscriptions.models import SprintSubscription, ATTSubscription
from wt.subscriptions.serializers import SprintSubscriptionSerializer, ATTSubscriptionSerializer, \
    ReachedAttSubscriptionSerializer, ReachedSprintSubscriptionSerializer
from wt.subscriptions.services import SubscriptionService


class SprintSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = SprintSubscription.objects.all()
    serializer_class = SprintSubscriptionSerializer


class ATTSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = ATTSubscription.objects.all()
    serializer_class = ATTSubscriptionSerializer


class ReachedSubscriptionsView(APIView):
    """
    Find any subscriptions that have reached the price limit on either data and/or voice
    """

    def get(self, request, *args, **kwargs):
        price_limit = float(request.query_params.get('price_limit', 0))
        context = {"price_limit": price_limit}
        att_subscription_serializer = ReachedAttSubscriptionSerializer(
            self.get_reached_att_subscriptions(price_limit),
            many=True,
            context=context
        )
        sprint_subscription_serializer = ReachedSprintSubscriptionSerializer(
            self.get_reached_sprint_subscriptions(price_limit),
            many=True,
            context=context
        )
        return Response({
            "att_subscriptions": att_subscription_serializer.data,
            "sprint_subscriptions": sprint_subscription_serializer.data
        })

    def get_reached_att_subscriptions(self, price_limit):
        subscription_service = SubscriptionService()
        att_subscriptions = ATTSubscription.objects.all()
        att_subscriptions_reached = subscription_service.find_subscriptions_reached_limit(
            att_subscriptions,
            price_limit
        )
        return att_subscriptions_reached

    def get_reached_sprint_subscriptions(self, price_limit):
        subscription_service = SubscriptionService()
        sprint_subscriptions = SprintSubscription.objects.all()
        sprint_subscriptions_reached = subscription_service.find_subscriptions_reached_limit(
            sprint_subscriptions,
            price_limit
        )
        return sprint_subscriptions_reached
