from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wt.subscriptions.models import SprintSubscription, ATTSubscription
from wt.subscriptions.factories import SprintSubscriptionFactory, ATTSubscriptionFactory, UserFactory
from wt.plans.factories import PlanFactory
from wt.usage.factories import DataUsageRecordFactory, VoiceUsageRecordFactory


class SubscriptionTests(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.plan = PlanFactory()
        self.sprint_subscription = SprintSubscriptionFactory()
        self.att_subscription = ATTSubscriptionFactory()

    def test_list_att_subscription(self):
        url = reverse("att_subscription-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sprint_subscription(self):
        url = reverse("split_subscription-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_att_subscription(self):
        url = reverse("att_subscription-list")
        data = {
            "user": self.user.id,
            "plan": self.plan.id,
            "status": ATTSubscription.STATUS.active,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reached_data_att_subscription(self):
        usage_counter = 5
        kilobytes_used = 5000
        price_limit = 5
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            att_subscription=self.att_subscription
        )
        url = reverse('reached_subscriptions')

        response = self.client.get(url, {'price_limit': price_limit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        att_sub_response = response.data.get('att_subscriptions')
        data_usage_price = usage_counter * kilobytes_used * ATTSubscription.ONE_KILOBYTE_PRICE
        self.assertEqual(att_sub_response[0].get('id'), self.att_subscription.id)
        self.assertEqual(att_sub_response[0].get('usage_type'), ['DataUsageRecord'])
        self.assertEqual(att_sub_response[0].get('data_exceeded_limit'), abs(data_usage_price - price_limit))

    def test_reached_voice_att_subscription(self):
        usage_counter = 5
        seconds_used = 511
        price_limit = 2
        VoiceUsageRecordFactory.create_batch(
            usage_counter,
            seconds_used=seconds_used,
            att_subscription=self.att_subscription
        )
        url = reverse('reached_subscriptions')

        response = self.client.get(url, {'price_limit': price_limit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        att_sub_response = response.data.get('att_subscriptions')
        second_usage_price = usage_counter * seconds_used * ATTSubscription.ONE_SECOND_PRICE
        self.assertEqual(att_sub_response[0].get('id'), self.att_subscription.id)
        self.assertEqual(att_sub_response[0].get('usage_type'), ['VoiceUsageRecord'])
        self.assertEqual(att_sub_response[0].get('voice_exceeded_limit'), abs(second_usage_price - price_limit))

    def test_reached_voice_sprint_subscription(self):
        usage_counter = 5
        seconds_used = 5000
        price_limit = 2
        VoiceUsageRecordFactory.create_batch(
            usage_counter,
            seconds_used=seconds_used,
            sprint_subscription=self.sprint_subscription
        )
        url = reverse('reached_subscriptions')

        response = self.client.get(url, {'price_limit': price_limit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        att_sub_response = response.data.get('sprint_subscriptions')
        second_usage_price = usage_counter * seconds_used * SprintSubscription.ONE_SECOND_PRICE
        self.assertEqual(att_sub_response[0].get('id'), self.att_subscription.id)
        self.assertEqual(att_sub_response[0].get('usage_type'), ['VoiceUsageRecord'])
        self.assertEqual(att_sub_response[0].get('voice_exceeded_limit'), abs(second_usage_price - price_limit))

    def test_reached_data_sprint_subscription(self):
        usage_counter = 5
        kilobytes_used = 2466
        price_limit = 5
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            sprint_subscription=self.sprint_subscription
        )
        url = reverse('reached_subscriptions')

        response = self.client.get(url, {'price_limit': price_limit})
        sprint_sub_response = response.data.get('sprint_subscriptions')
        data_usage_price = usage_counter * kilobytes_used * SprintSubscription.ONE_KILOBYTE_PRICE
        self.assertEqual(sprint_sub_response[0].get('id'), self.sprint_subscription.id)
        self.assertEqual(sprint_sub_response[0].get('usage_type'), ['DataUsageRecord'])
        self.assertEqual(sprint_sub_response[0].get('data_exceeded_limit'), abs(data_usage_price - price_limit))

    def test_reached_subscriptions_limit_not_set(self):
        usage_counter = 1
        kilobytes_used = 1234
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            sprint_subscription=self.sprint_subscription
        )
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            att_subscription=self.att_subscription
        )
        url = reverse('reached_subscriptions')
        response = self.client.get(url)
        count_att_sub_with_data_usage = ATTSubscription.objects.filter(datausagerecord__isnull=False).count()
        count_sprint_sub_with_data_usage = SprintSubscription.objects.filter(datausagerecord__isnull=False).count()
        sprint_sub_response = response.data.get('sprint_subscriptions')
        att_sub_response = response.data.get('att_subscriptions')
        self.assertEqual(len(att_sub_response), count_att_sub_with_data_usage)
        self.assertEqual(len(sprint_sub_response), count_sprint_sub_with_data_usage)

    def test_reached_subscriptions_data_and_voice(self):
        usage_counter = 5
        kilobytes_used = 2466
        price_limit = 2
        seconds_used = 5000
        VoiceUsageRecordFactory.create_batch(
            usage_counter,
            seconds_used=seconds_used,
            sprint_subscription=self.sprint_subscription
        )
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            sprint_subscription=self.sprint_subscription
        )
        url = reverse('reached_subscriptions')
        response = self.client.get(url, {'price_limit': price_limit})
        sprint_sub_response = response.data.get('sprint_subscriptions')
        data_usage_price = usage_counter * kilobytes_used * SprintSubscription.ONE_KILOBYTE_PRICE
        second_usage_price = usage_counter * seconds_used * SprintSubscription.ONE_SECOND_PRICE
        self.assertEqual(sprint_sub_response[0].get('id'), self.sprint_subscription.id)
        self.assertEqual(sprint_sub_response[0].get('usage_type'), ['DataUsageRecord', 'VoiceUsageRecord'])
        self.assertEqual(sprint_sub_response[0].get('data_exceeded_limit'), abs(data_usage_price - price_limit))
        self.assertEqual(sprint_sub_response[0].get('voice_exceeded_limit'), abs(second_usage_price - price_limit))

    def test_negative_subscriptions_data_and_voice(self):
        usage_counter = 5
        kilobytes_used = 2466
        price_limit = -5
        seconds_used = 5000
        VoiceUsageRecordFactory.create_batch(
            usage_counter,
            seconds_used=seconds_used,
            sprint_subscription=self.sprint_subscription
        )
        DataUsageRecordFactory.create_batch(
            usage_counter,
            kilobytes_used=kilobytes_used,
            sprint_subscription=self.sprint_subscription
        )
        url = reverse('reached_subscriptions')
        response = self.client.get(url, {'price_limit': price_limit})
        sprint_sub_response = response.data.get('sprint_subscriptions')
        data_usage_price = usage_counter * kilobytes_used * SprintSubscription.ONE_KILOBYTE_PRICE
        second_usage_price = usage_counter * seconds_used * SprintSubscription.ONE_SECOND_PRICE
        self.assertEqual(sprint_sub_response[0].get('id'), self.sprint_subscription.id)
        self.assertEqual(sprint_sub_response[0].get('usage_type'), ['DataUsageRecord', 'VoiceUsageRecord'])
        self.assertEqual(sprint_sub_response[0].get('data_exceeded_limit'), abs(data_usage_price - price_limit))
        self.assertEqual(sprint_sub_response[0].get('voice_exceeded_limit'), abs(second_usage_price - price_limit))

