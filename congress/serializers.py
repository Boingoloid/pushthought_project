from rest_framework import serializers
from . import models


class CongressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Congress
        fields = ('title', 'twitter_id', 'phone', 'oc_email', 'full_name', 'image')