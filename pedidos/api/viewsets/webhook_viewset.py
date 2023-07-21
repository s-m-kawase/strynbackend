
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


stripe.api_key = config('STRIPE_SECRET_KEY')
# endpoint_secret = config('STRIPE_WEBHOOK_SECRET')

class StripeWebhookViewSet(ViewSet):

  def update_order_status(self, pedido ,session):
    email = session['customer_details']['email']
    if session['status'] == 'complete':
        pedido.status_pedido = 'Pago'
        pedido.save()

        # # mensagem detalhes do pedido
        # message = f"Seu pagamento foi processado com sucesso. Obrigado por sua compra!\n\n"
        # message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nValor Total: {pedido.total}\nStatus do Pedido: {pedido.status_pedido}"
        # # Enviar uma confirmação por e-mail
        # remetente = settings.EMAIL_HOST_USER
        # recipient_email = email
        # subject = 'Confirmação de Pagamento'

        # send_mail(subject, message, remetente, [recipient_email])

        # ConfirmarPagamento = namedtuple(
        #    "confimar_pagamento_object", ['id','pedido']
        # )

        # confimar_pagamento_object = ConfirmarPagamento(
        #     id=0,
        #     pedido=pedido,
        # )

        try:
            template_email = TemplateEmail.objects.filter(
                codigo="confirma_pagamento"
            ).first()

            if not template_email:
                raise ValueError(
                    "Serviço indisponível, contate seu administrador!"
                )
            mensagem_email = MensagemEmail.objects.create(
                template_email=template_email
            )
            
            mensagem_email.enviar(pedido)

            return JsonResponse(
                {
                    "status": "200",
                    "message": "Email enviado com sucesso!",
                }
            )
        except Exception as error:
            return JsonResponse(
                {
                    "status": "404",
                    "message": error.args[0],
                }
            )


  def cancel_checkout_session(self, pedido, session):

      email = session['customer_details']['email']
      pedido.status_pedido = 'Cancelado'
      pedido.save()

      # Notificar o cliente sobre o cancelamento do pedido
      remetente = settings.EMAIL_HOST_USER
      recipient_email = email
      subject = 'saldo insuficiente'
      message = f"Seu pagamento foi cancelado. Entre em contato conosco para obter mais informações.\n\n"
      message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nStatus do Pedido: {pedido.status_pedido}\n"
      send_mail(subject, message, remetente, [recipient_email])


  def handle_payment_failed(self, pedido, payment_intent):
      email = payment_intent['charges']['data'][0]['billing_details']['email']


      # Atualizar o status do pedido
      pedido.status_pedido = 'Com erro'
      pedido.save()

      # Enviar um e-mail ao cliente informando sobre o pagamento falhado
      remetente = settings.EMAIL_HOST_USER
      recipient_email = email
      subject = 'Falha no Pagamento'
      message = 'O pagamento do seu pedido falhou. Por favor, tente novamente.'
      send_mail(subject, message, remetente, [recipient_email])


  """ def handle_charge_refunded(refund, payment_intent_id):
      pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
      if pedido.status_pedido == 'Estornado':
        # Enviar email
        remetente = settings.EMAIL_HOST_USER
        recipient_email = refund['billing_details']['email']
        subject = 'Estorno do Pedido'
        message = 'O pagamento do seu pedido foi estornado. Entre em contato conosco para mais informações.'
        send_mail(subject, message, remetente, [recipient_email])

        return Response({'mensagem': 'Estorno realizado com sucesso'}, status=200)
 """

  @action(detail=False, methods=['post'])
  def initiate_payment(self, request):
        session_id = request.data.get('session_id')
        self.process_payment(session_id)
        return Response({'message': 'Pagamento processado com sucesso'})

  @action(detail=False, methods=['get'])
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

        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']
            session_id = session['id']
            pedido = Pedidos.objects.get(session_id=session_id)
            self.cancel_checkout_session(pedido, session)

        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment_intent_id = payment_intent['id']
            pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
            self.handle_payment_failed(pedido, payment_intent)


        elif event['type'] == 'charge.refunded':
          payment_intent_id = event['data']['object']['payment_intent']
          pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
          if pedido.status_pedido == 'Cancelado':
              # Enviar email
              remetente = settings.EMAIL_HOST_USER
              recipient_email = event['data']['object']['billing_details']['email']
              subject = 'Estorno do Pedido'
              message = 'O pagamento do seu pedido foi estornado. Entre em contato conosco para mais informações.'
              send_mail(subject, message, remetente, [recipient_email])

          return Response({'mensagem': 'Estorno realizado com sucesso'}, status=200)




        return Response(status=200)


