from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ...models import ConfigStripe
from ..serializers.config_stripe_seriaçizer import ConfigStripeSerializer


class ConfigStripeViewSet(viewsets.ModelViewSet):
    queryset = ConfigStripe.objects.all()
    serializer_class = ConfigStripeSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        
    ]
