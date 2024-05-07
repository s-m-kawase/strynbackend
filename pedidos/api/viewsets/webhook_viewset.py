
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


stripe.api_key = config('STRIPE_SECRET_KEY')
# endpoint_secret = config('STRIPE_WEBHOOK_SECRET')

class StripeWebhookViewSet(ViewSet):

  def update_order_status(self, pedido ,session):
    email = session['customer_details']['email']
    if session['status'] == 'complete':
        pedido.status_pedido = 'Aguardando Confirmação'
        pedido.hora_status_pago = timezone.now()
        pedido.save()

        try:
            template_email = TemplateEmail.objects.filter(
                codigo='confirma_pagamento'
            ).first()

            if not template_email:
                raise ValueError(
                    "Serviço indisponível, contate seu administrador!"
                )
            mensagem_email = MensagemEmail.objects.create(
                template_email=template_email
            )

            mensagem_email.enviar(pedido, [email])


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

    #   # Notificar o cliente sobre o cancelamento do pedido
    #   remetente = settings.EMAIL_HOST_USER
    #   recipient_email = email
    #   subject = 'saldo insuficiente'
    #   message = f"Seu pagamento foi cancelado. Entre em contato conosco para obter mais informações.\n\n"
    #   message += f"Detalhes do pedido:\n\nID do Pedido: {pedido.id}\nStatus do Pedido: {pedido.status_pedido}\n"
    #   send_mail(subject, message, remetente, [recipient_email])
        try:
                template_email = TemplateEmail.objects.filter(
                    codigo='pagamento_cancelado'
                ).first()

                if not template_email:
                    raise ValueError(
                        "Serviço indisponível, contate seu administrador!"
                    )
                mensagem_email = MensagemEmail.objects.create(
                    template_email=template_email
                )
                
                mensagem_email.enviar(pedido, [email])
                

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


  def handle_payment_failed(self, pedido, payment_intent):
    email = payment_intent['charges']['data'][0]['billing_details']['email']


    # Atualizar o status do pedido
    pedido.status_pedido = 'Com erro'
    pedido.save()

    #   # Enviar um e-mail ao cliente informando sobre o pagamento falhado
    #   remetente = settings.EMAIL_HOST_USER
    #   recipient_email = email
    #   subject = 'Falha no Pagamento'
    #   message = 'O pagamento do seu pedido falhou. Por favor, tente novamente.'
    #   send_mail(subject, message, remetente, [recipient_email])

    try:
        template_email = TemplateEmail.objects.filter(
            codigo='falha_pagamento'
        ).first()

        if not template_email:
            raise ValueError(
                "Serviço indisponível, contate seu administrador!"
            )
        mensagem_email = MensagemEmail.objects.create(
            template_email=template_email
        )
        
        mensagem_email.enviar(pedido, [email])
        

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
            pedido.payment_intent_id = session['payment_intent']
            pedido.save()
            self.update_order_status(pedido, session)

        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']
            session_id = session['id']
            pedido = Pedidos.objects.get(session_id=session_id)
            self.cancel_checkout_session(pedido, session)

        # elif event['type'] == 'payment_intent.created':
        #     session = event['data']['object']['id']
        #     session_id = session['id']
        #     pedido = Pedidos.objects.get(session_id=session_id)

        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment_intent_id = payment_intent['id']
            pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
            self.handle_payment_failed(pedido, payment_intent)


        elif event['type'] == 'charge.refunded':
          payment_intent_id = event['data']['object']['payment_intent']
          pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
          if pedido.status_pedido == 'Cancelado':
            #   # Enviar email
            #   remetente = settings.EMAIL_HOST_USER
            #   subject = 'Estorno do Pedido'
            #   message = 'O pagamento do seu pedido foi estornado. Entre em contato conosco para mais informações.'
            #   send_mail(subject, message, remetente, [recipient_email])
            email = event['data']['object']['billing_details']['email']
            try:
                template_email = TemplateEmail.objects.filter(
                    codigo='reembolso_pedido'
                ).first()

                if not template_email:
                    raise ValueError(
                        "Serviço indisponível, contate seu administrador!"
                    )
                mensagem_email = MensagemEmail.objects.create(
                    template_email=template_email
                )
                
                mensagem_email.enviar(pedido, [email])
                

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
          return Response({'mensagem': 'Estorno realizado com sucesso'}, status=200)
            
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent_id = event['data']['object']['id']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            charge_id = payment_intent['charges']['data'][0]['id']
            pedido = Pedidos.objects.get(payment_intent_id=payment_intent_id)
            # return JsonResponse({
            #     "pedido_id": pedido.id,
            #     "pedido": pedido.payment_intent_id,
            #     "payment_intent_id": payment_intent_id,
            #     "charge_id": charge_id,
            #                      })
            
            if pedido:
                total_split = pedido.total_split
                porcentagem_em_decimal = pedido.restaurante.pocentagem_para_tranferencia / 100
                taxa_atendimento = pedido.taxa_de_atendimento if pedido.taxa_de_atendimento else 0
                valor_para_conta_conectada = total_split * porcentagem_em_decimal
                valor_para_conta_conectada += taxa_atendimento
                # valor_para_conta_conectada /= 100  # Convertendo para reais

                return JsonResponse({
                "pedido_id": pedido.id,
                "pedido": pedido.payment_intent_id,
                "charge_id": charge_id,
                "total_split": total_split,
                "porcentagem_em_decimal": porcentagem_em_decimal,
                "taxa_atendimento": taxa_atendimento,
                "valor_para_conta_conectada": valor_para_conta_conectada,
                })
                    
                    # try:
                    #     stripe.Transfer.create(
                    #         amount=int(valor_para_conta_conectada * 100),  # Valor em centavos
                    #         currency='brl',
                    #         destination=pedido.restaurante.chave_connect,
                    #         description=f'Transferência para conta conectada {pedido.restaurante.nome}',
                    #         source_transaction=charge_id,
                    #     )
                    # except stripe.error.StripeError as e:
                    #     return JsonResponse({"Erro": str(e)})
                # else:
                #     return JsonResponse({"Erro": "Pedido não encontrado."})
           

        return Response(status=200)


