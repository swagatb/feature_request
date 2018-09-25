from rest_framework import serializers
from xceedance.models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("title", "description",
                  "client", "client_priority",
                  "target_date", "product_area")

    def create(self, validated_data):
        feature = Feature.objects.create(reporter=self.context['request'].user,
                                         **validated_data)
        return feature
