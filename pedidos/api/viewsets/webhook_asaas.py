import stripe
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
from django.views import View
import hmac
import hashlib

asaas_api = config('ASAAS_API_KEY')

class AsaasWebhookViewSet(ViewSet):

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def webhook(self, request):
        # Obtenha os dados do webhook do corpo da solicitação
        payload = request.data

        # Verifique se o evento é um evento válido do Asaas
        event_type = payload.get('event_type')

        if event_type == 'PAYMENT_CREATED':
            payment_data = payload['payment']
            pedido_id = payment_data['externalReference']
            self.update_pedido_status(pedido_id)

        

        return JsonResponse({'message': 'Webhook recebido com sucesso'})

    def update_pedido_status(self, pedido_id):
        pedido = Pedidos.objects.get(id=pedido_id)
        pedido.status_pedido = 'Pago'
        pedido.hora_status_pago = timezone.now()
        pedido.save()
        


        

    # @csrf_exempt
    # def post(self, request):
    #     endpoint_secret = config('ASAAS_API_SECRET')
    #     secret_key = bytes(endpoint_secret, 'utf-8')
        
    #     # Verifique a assinatura do webhook para garantir que os dados não foram adulterados
    #     received_signature = request.headers.get('X-Asaas-Signature')
    #     computed_signature = hmac.new(secret_key, request.body, hashlib.sha256).hexdigest()

    #     if received_signature != computed_signature:
    #         return JsonResponse({'message': 'Assinatura inválida'}, status=400)

    #     # O webhook é válido, você pode processar os dados aqui
    #     data = request.body.decode('utf-8')
    #     # Faça o processamento necessário com os dados do webhook
    #     if 'event' in data and data['event'] == 'PAYMENT_CREATED':
    #         payment_data = data['data']  # Suponha que os dados do pagamento estejam no campo 'data'
    #         pedido_id = payment_data['pedido_id']  # Suponha que o ID do pedido esteja nos dados do pagamento
    #         novo_status = 'Pago'  # Suponha que você queira atualizar para o status 'Pago'

    #         pedido = update_pedido_status(pedido_id, novo_status)
    #         if pedido:
    #             # Pedido atualizado com sucesso
    #             # Você pode retornar uma resposta de sucesso aqui
    #         else:
    #             # Pedido não encontrado
    #             # Retorne uma resposta de erro, se apropriado
    #     return JsonResponse({'message': 'Webhook recebido com sucesso'})