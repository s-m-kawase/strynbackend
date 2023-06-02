# from django.http import HttpResponseRedirect
# import stripe
# from rest_framework import filters, viewsets
# from rest_framework.permissions import IsAuthenticated
# from ...models import Price
# from ..serializers.price_serializer import PriceSerializer
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import redirect
# from decouple import config
# from django.contrib import messages



# class PriceViewSet(viewsets.ModelViewSet):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer
#     # permission_classes = [IsAuthenticated]

#     filter_backends = [filters.SearchFilter]

#     search_fields = [
        
#     ]


#     @action(detail=True, methods=['post'])
#     def create_checkout_session(self, request, pk):
#         stripe_secret_key = config('STRIPE_SECRET_KEY')
#         stripe.api_key = stripe_secret_key

#         price_id = Price.objects.get(id=pk)
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price': price_id.stripe_price_id,
#                     'quantity': price_id.quantidade,
#                 },
#             ],
#             mode='payment',
#             success_url='http://localhost:8000/success',
#             cancel_url='http://localhost:8000/cancel',
#         )
#         messages.success(request, 'Redirecionamento realizado com sucesso.')
#         return redirect(checkout_session.url)
