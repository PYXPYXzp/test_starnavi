from rest_framework import serializers
from wt.subscriptions.models import SprintSubscription, ATTSubscription


class SprintSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SprintSubscription
        fields = "__all__"


class ATTSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ATTSubscription
        fields = "__all__"


class BaseReachedSubscriptionsSerializer(serializers.ModelSerializer):
    usage_type = serializers.SerializerMethodField()
    data_exceeded_limit = serializers.SerializerMethodField()
    voice_exceeded_limit = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_usage_type(self, obj):
        usage_types = []
        if obj.data_exceeded_limit and obj.data_exceeded_limit < 0:
            usage_types.append('DataUsageRecord')
        if obj.voice_exceeded_limit and obj.voice_exceeded_limit < 0:
            usage_types.append('VoiceUsageRecord')
        return usage_types

    def get_data_exceeded_limit(self, obj):
        if obj.data_exceeded_limit and obj.data_exceeded_limit < 0:
            return abs(obj.data_exceeded_limit)
        return 0

    def get_voice_exceeded_limit(self, obj):
        if obj.voice_exceeded_limit and obj.voice_exceeded_limit < 0:
            return abs(obj.voice_exceeded_limit)
        return 0


class ReachedAttSubscriptionSerializer(BaseReachedSubscriptionsSerializer):

    class Meta:
        model = ATTSubscription
        fields = ("id", "usage_type", "data_exceeded_limit", "voice_exceeded_limit")


class ReachedSprintSubscriptionSerializer(BaseReachedSubscriptionsSerializer):

    class Meta:
        model = SprintSubscription
        fields = ("id", "usage_type", "data_exceeded_limit", "voice_exceeded_limit")
