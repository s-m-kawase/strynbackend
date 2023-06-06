
import stripe
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from pedidos.models import Pedidos
from decouple import config


stripe.api_key = config('STRIPE_SECRET_KEY')
# endpoint_secret = config('STRIPE_WEBHOOK_SECRET')

class StripeWebhookViewSet(ViewSet):

    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        session_id = request.data.get('session_id')
        self.process_payment(session_id)
        return Response({'message': 'Pagamento processado com sucesso'})

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def webhook(self, request):
       
        endpoint_secret = config('STRIPE_WEBHOOK_SECRET')
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Se payload for inválido, retorna erro 400
            return Response(status=400, data={
                'error': 'Erro no payload',
                'message': f"{e}",
                #  'requet_meta':request.META,
                'requet_data':request.data,
                'assinatura_cabecalho':sig_header,
                })
        except stripe.error.SignatureVerificationError as e:
            # Se a assinatura for inválida, retorna erro 400
            return Response(status=400, data={
                'error': 'Assinatura inválida',
                'message': f"{e}",
                # 'requet_meta':request.META,
                'requet_data':request.data,
                'assinatura_cabecalho':sig_header,
                })

        # Lidar com o evento
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            session_id = event['data']['object']['id']          
            pedido = Pedidos.objects.get(session_id=session_id)
            self.update_order_status(pedido, session)

        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            session_id = event['data']['object']['id']          
            pedido = Pedidos.objects.get(session_id=session_id)
            status = payment_intent['status']
            self.confirma_pagamento(pedido, payment_intent, status)
                    

        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            session_id = event['data']['object']['id']  
            pedido = Pedidos.objects.get(session_id=session_id)
            self.handle_failed_payment(payment_intent, pedido)
            

        return Response(status=200)


    def update_order_status(self, pedido ,session):
        email = session['customer_details']['email']
        if session['status'] == 'complete':
            pedido.status_pedido = 'Pago'
            pedido.save()

            # mensagem detalhes do pedido
            message = f"Seu pagamento foi processado com sucesso. Obrigado por sua compra!\n\n"
            message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nValor Total: {pedido.total}\nStatus do Pedido: {pedido.status_pedido}"
            # Enviar uma confirmação por e-mail
            remetente = settings.EMAIL_HOST_USER
            recipient_email = email
            subject = 'Confirmação de Pagamento'
            
            send_mail(subject, message, remetente, [recipient_email])

        elif session['status'] == 'incomplete':
            pedido.status_pedido = 'Sacola'
            pedido.save()

            # Enviar um lembrete de pagamento, agendar uma nova tentativa de cobrança, etc.
            remetente = config('EMAIL_HOST_USER')
            recipient_email = email
            subject = 'Lembrete de Pagamento'
            message = f"Seu pagamento está incompleto. Por favor, verifique as informações do seu pagamento e conclua a transação para prosseguir com o pedido.\n\n"
            message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nStatus do Pedido: {pedido.status_pedido}\n"
            send_mail(subject, message, remetente, [recipient_email])

        elif session['status'] == 'canceled':
            pedido.status_pedido = 'Cancelado'
            pedido.save()

            # Notificar o cliente sobre o cancelamento do pedido
            remetente = config('EMAIL_HOST_USER')
            recipient_email = email
            subject = 'Cancelamento de Pedido'
            message = f"Seu pagamento foi cancelado. Entre em contato conosco para obter mais informações.\n\n"
            message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nStatus do Pedido: {pedido.status_pedido}\n"
            send_mail(subject, message, remetente, [recipient_email])
    

    def confirma_pagamento(self, pedido, payment_intent, status):
        email = payment_intent['charges']['data'][0]['billing_details']['email']

        if status == 'succeeded':
            pedido.status_pedido = 'Pago'
            pedido.save()

            # mensagem detalhes do pedido
            message = f"Seu pagamento foi processado com sucesso. Obrigado por sua compra!\n\n"
            message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nValor Total: {pedido.total}\nStatus do Pedido: {pedido.status_pedido}"
            # Enviar uma confirmação por e-mail
            remetente = settings.EMAIL_HOST_USER
            recipient_email = email
            subject = 'Confirmação de Pagamento'
            
            send_mail(subject, message, remetente, [recipient_email])
            
                
            # Gerar uma nota fiscal


    def handle_failed_payment(self, pedido ,payment_intent):
        try:

            # Atualizar o status do pedido
            pedido.status_pedido = 'Com erro'
            pedido.save()

            # Enviar um e-mail ao cliente informando sobre o pagamento falhado
            remetente = config('EMAIL_HOST_USER')
            destinatario = pedido.cliente.user.email
            assunto = 'Falha no Pagamento'
            mensagem = 'O pagamento do seu pedido falhou. Por favor, tente novamente.'
            send_mail(assunto, mensagem, remetente, [destinatario])

        except Pedidos.DoesNotExist:
            # Pedido não encontrado
            return Response(status=400, data={'error': 'Pedido não encontrado'})

        except Exception as e:
            # Outro erro durante o tratamento do pagamento falhado
            return Response(status=500, data={'error': 'Erro ao lidar com o pagamento falhado'})
