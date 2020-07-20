from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from wt.subscriptions.views import ATTSubscriptionViewSet, SprintSubscriptionViewSet, ReachedSubscriptionsView

router = routers.DefaultRouter()

router.register(r'att_subscriptions', ATTSubscriptionViewSet, base_name='att_subscription')
router.register(r'sprint_subscriptions', SprintSubscriptionViewSet, base_name='split_subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('reached_subscriptions/', ReachedSubscriptionsView.as_view(), name='reached_subscriptions'),
]
