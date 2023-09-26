import stripe
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from pedidos.models import Pedidos
from decouple import config
from emails.models import MensagemEmail, TemplateEmail
from collections import namedtuple
from django.http import JsonResponse
from django.utils import timezone


stripe.api_key = config('ASAAS_API_KEY')

class AsaasWebhookViewSet(ViewSet):


    @action(detail=False, methods=['get'])
    @csrf_exempt
    def webhook(self, request):

        endpoint_secret = config('ASAAS_API_SECRET')
        payload = request.body
        event = None