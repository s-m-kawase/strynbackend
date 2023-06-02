
import json
import stripe
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from pedidos.models import Pedidos
from apistripe.models.stripe import Stripe

from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY')
# endpoint_secret = config('STRIPE_WEBHOOK_SECRET')


class StripeWebhookViewSet(ViewSet):
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def webhook(self, request):
        endpoint_secret = 'whsec_ZAzKGVyqFlX4qOaRgFPCRbSiwSALukQL'

        payload = request.data
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
             return Response(status=400, data={
                'error': 'Erro no payload',
                'endpoint': endpoint_secret,
                'message': f"{e}",
                #  'requet_meta':request.META,
                'payload':request.data,
                'HTTP_STRIPE_SIGNATURE':sig_header,
                })
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400, data={
                'error': 'Erro no payload',
                'message': f"{e}",
                #  'requet_meta':request.META,
                'requet_data':request.data,
                'assinatura_cabecalho':sig_header,
                })

        # Passed signature verification
        return Response(status=200)




    # @action(detail=False, methods=['post'])
    # def initiate_payment(self, request):
    #     session_id = request.data.get('session_id')
    #     self.process_payment(session_id)
    #     return Response({'message': 'Pagamento processado com sucesso'})

    # @action(detail=False, methods=['post'])
    # @csrf_exempt
    # def webhook(self, request):
    #     # stripe = Stripe.objects.all().first()
    #     # stripe.request_data = request.data
    #     # stripe.webhook = request.META
    #     # stripe.save()
    #     endpoint_secret = 'whsec_ZAzKGVyqFlX4qOaRgFPCRbSiwSALukQL'
    #     payload = request.data
    #     sig_header = 't=1685708166,v1=d2e6d2410b53c49a9afd2806dae8de9c72ae718d9ee8b5b957c9c3b0f80eced1,v0=0897b4891b49b2aba45e424938809633e65df1ee4481b0b6880c123cd0c93524'
    #     event = None

    #     try:
    #         event = stripe.Webhook.construct_event(
    #             payload, sig_header, endpoint_secret
    #         )
    #     except ValueError as e:
    #         # Se payload for inválido, retorna erro 400
    #         return Response(status=400, data={
    #             'error': 'Erro no payload',
    #             'message': f"{e}",
    #             #  'requet_meta':request.META,
    #             'requet_data':request.data,
    #             'assinatura_cabecalho':sig_header,
    #             })
    #     except stripe.error.SignatureVerificationError as e:
    #         # Se a assinatura for inválida, retorna erro 400
    #         return Response(status=400, data={
    #             'error': 'Assinatura inválida',
    #             'message': f"{e}",
    #             # 'requet_meta':request.META,
    #             'requet_data':request.data,
    #             'assinatura_cabecalho':sig_header,
    #             })

    #     # Lidar com o evento
    #     if event['type'] == 'checkout.session.completed':
    #         session = event['data']['object']
    #         self.update_order_status(session)

    #     elif event['type'] == 'payment_intent.succeeded':
    #         payment_intent = event['data']['object']
    #         self.update_order_status(payment_intent)

    #     elif event['type'] == 'payment_intent.payment_failed':
    #         payment_intent = event['data']['object']
    #         self.handle_failed_payment(payment_intent)

    #     return Response(status=200)


    # def update_order_status(self, session):
    #     try:
    #         # Obter o pedido associado ao session_id
    #         pedido = Pedidos.objects.get(session_id=session['id'])

    #         # Obter o e-mail do cliente a partir do modelo User
    #         cliente_email = pedido.cliente.user.email

    #         # Atualizar o status do pedido com base no pagamento
    #         if session['payment_status'] == 'paid':
    #             pedido.status = 'Pago'

    #             # Enviar uma confirmação por e-mail
    #             remetente = config('EMAIL_HOST_USER')
    #             recipient_email = cliente_email
    #             subject = 'Confirmação de Pagamento'
    #             message = 'Seu pagamento foi processado com sucesso. Obrigado por sua compra! \n Aguarde sua entrega está a caminho!'
    #             send_mail(subject, message, remetente, [recipient_email])

    #             # Gerar uma nota fiscal

    #         elif session['payment_status'] == 'unpaid':
    #             pedido.status = 'Sacola'
    #             # Enviar um lembrete de pagamento, agendar uma nova tentativa de cobrança, etc.
    #             remetente = config('EMAIL_HOST_USER')
    #             recipient_email = cliente_email
    #             subject = 'Lembrete de Pagamento'
    #             message = 'Lembramos que o Pagamento do seu pedido ainda está pendente. Por favor, realize o pagamento o mais breve possível.'
    #             send_mail(subject, message, remetente, [recipient_email])

    #         elif session['payment_status'] == 'canceled':
    #             pedido.status = 'Cancelado'
    #             # Notificar o cliente sobre o cancelamento do pedido
    #             remetente = config('EMAIL_HOST_USER')
    #             recipient_email = cliente_email
    #             subject = 'Cancelamento de Pedido'
    #             message = 'Infelizmente, o seu pedido foi cancelado. Entre em contato conosco para mais informações.'
    #             send_mail(subject, message, remetente, [recipient_email])

    #         # Salvar as alterações no pedido
    #         pedido.save()

    #     except Pedidos.DoesNotExist:
    #         # Pedido não encontrado
    #         return Response(status=400, data={'error': 'Pedido não encontrado'})

    #     except Exception as e:
    #         # Outro erro durante a atualização do status do pedido
    #         return Response(status=500, data={'error': 'Erro ao atualizar o status do pedido'})


    # def handle_failed_payment(self, payment_intent):
    #     try:
    #         # Lógica para lidar com o pagamento falhado, por exemplo, enviar um e-mail ao cliente
    #         pedido = Pedidos.objects.get(session_id=payment_intent['id'])

    #         # Atualizar o status do pedido
    #         pedido.status = 'Com erro'
    #         pedido.save()

    #         # Enviar um e-mail ao cliente informando sobre o pagamento falhado
    #         remetente = config('EMAIL_HOST_USER')
    #         destinatario = pedido.cliente.user.email
    #         assunto = 'Falha no Pagamento'
    #         mensagem = 'O pagamento do seu pedido falhou. Por favor, tente novamente.'
    #         send_mail(assunto, mensagem, remetente, [destinatario])

    #     except Pedidos.DoesNotExist:
    #         # Pedido não encontrado
    #         return Response(status=400, data={'error': 'Pedido não encontrado'})

    #     except Exception as e:
    #         # Outro erro durante o tratamento do pagamento falhado
    #         return Response(status=500, data={'error': 'Erro ao lidar com o pagamento falhado'})
