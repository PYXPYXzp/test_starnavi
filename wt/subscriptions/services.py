from django.db.models import QuerySet, Sum, Q, F, DecimalField, Subquery
from django.db.models.functions import Cast


class SubscriptionService:

    def find_subscriptions_reached_limit(self, subscriptions: QuerySet, limit: float) -> QuerySet:
        annotated_subscriptions = self.annotate_usages_price(subscriptions)
        reached_subscriptions = self.filter_reached_price_sbuscriptions(annotated_subscriptions, limit)
        return self.annotate_exceeded_limit(reached_subscriptions, limit)

    def annotate_usages_price(self, subscriptions: QuerySet) -> QuerySet:
        subscription_model = subscriptions.model
        data_usage_price = subscriptions.annotate(
            data_usage_price=Cast(
                Sum('datausagerecord__kilobytes_used') * subscription_model.ONE_KILOBYTE_PRICE,
                DecimalField()
            )
        )
        voice_usage_price = subscriptions.annotate(
            voice_usage_price=Cast(
                Sum('voiceusagerecord__seconds_used') * subscription_model.ONE_SECOND_PRICE,
                DecimalField()
            )
        )
        subscriptions = subscriptions.annotate(
            data_usage_price=Subquery(data_usage_price.values('data_usage_price'), output_field=DecimalField()),
            voice_usage_price=Subquery(voice_usage_price.values('voice_usage_price'), output_field=DecimalField())
        )
        return subscriptions

    def filter_reached_price_sbuscriptions(self, subscriptions: QuerySet, limit: float) -> QuerySet:
        subscriptions = subscriptions.filter(Q(data_usage_price__gte=limit) | Q(voice_usage_price__gte=limit))
        return subscriptions

    def annotate_exceeded_limit(self,subscriptions: QuerySet, limit: float) -> QuerySet:
        subscriptions = subscriptions.annotate(
            data_exceeded_limit=limit - F('data_usage_price'),
            voice_exceeded_limit=limit - F('voice_usage_price')
        )
        return subscriptions
