from rest_framework import serializers
from rest_framework.fields import empty
from . import models


class CongressSerializer(serializers.ModelSerializer):
    sent_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Congress
        fields = ('title', 'twitter_id', 'twitter', 'phone', 'oc_email', 'full_name', 'image', 'sent_messages_count','bioguide_id', 'district', 'state')

    def __init__(self, instance=None, data=empty, program_id=None, **kwargs):
        self.program_id = program_id
        super(CongressSerializer, self).__init__(instance, data, **kwargs)


    def get_sent_messages_count(self, obj):
        if not self.program_id:
            try:
                counter = obj.congresscounter_set.get(program__isnull=True, campaign__isnull=True).counter
            except models.CongressCounter.DoesNotExist:
                counter = 0
        else:
            try:
                counter = obj.congresscounter_set.get(program=self.program_id).counter
            except models.CongressCounter.DoesNotExist:
                counter = 0

        return counter


class CongressCampaignSerializer(serializers.ModelSerializer):
    sent_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Congress
        fields = ('title', 'twitter_id','twitter', 'phone', 'oc_email', 'full_name', 'image', 'sent_messages_count',
                  'bioguide_id', 'district', 'state')

    def __init__(self, instance=None, data=empty, program_id=None, **kwargs):
        self.program_id = program_id
        super(CongressCampaignSerializer, self).__init__(instance, data, **kwargs)

    def get_sent_messages_count(self, obj):
        try:
            counter = obj.congresscounter_set.get(campaign__slug=self.program_id).counter
        except models.CongressCounter.DoesNotExist:
            counter = 0

        return counter