from rest_framework import serializers
from prime.models import SegmentAPI, LANGUAGE_CHOICES, STYLE_CHOICES


class SegmentAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = SegmentAPI
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return SegmentAPI.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance