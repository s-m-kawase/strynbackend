from rest_framework import serializers

from ...models import ConfigStripe


class ConfigStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigStripe
        fields = '__all__'
