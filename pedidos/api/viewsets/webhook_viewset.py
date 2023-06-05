
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
            pedido_id = session.get('metadata', {}).get('pedido_id')
            if pedido_id:
                pedido = Pedidos.objects.get(id=pedido_id)
                self.update_order_status(pedido, session)
            

        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            session_id = payment_intent.get('metadata', {}).get('session_id')
            if session_id:
                pedido = Pedidos.objects.get(session_id=session_id)
                self.handle_failed_payment(payment_intent, pedido)
            

        return Response(status=200)


    def update_order_status(self, pedido ,session):
   
        if session['payment_status'] == 'paid':
            customer_id = session['customer']['id']
            customer = stripe.Customer.retrieve(customer_id)
            cliente_email = customer['email']
            pedido.status_pedido = 'Pago'

            # lista dos item pedido
            # items = []
            # for item in pedido.itens_pedido.all():
            #     item_info = f"Nome do Item: {item.item.nome}\nQuantidade: {item.quantidade}\nPreço Unitário: {item.preco}\n\n"
            #     items.append(item_info)

            # # mensagem detalhes do pedido
            # message = f"Seu pagamento foi processado com sucesso. Obrigado por sua compra!\n\nDetalhes do pedido:\n\nID do Pedido: {pedido.id}\nValor Total: {pedido.total}\nStatus do Pedido: {pedido.status_pedido}\n\nItens do Pedido:\n"
            # # message += "\n".join(items)
            
            # # Enviar uma confirmação por e-mail
            # remetente = settings.EMAIL_HOST_USER
            # recipient_email = cliente_email
            # subject = 'Confirmação de Pagamento'
            
            # send_mail(subject, message, remetente, [recipient_email])
            
                
            # Gerar uma nota fiscal

        elif session['payment_status'] == 'unpaid':
            pedido.status_pedido = 'Sacola'
            # Enviar um lembrete de pagamento, agendar uma nova tentativa de cobrança, etc.
            remetente = config('EMAIL_HOST_USER')
            recipient_email = cliente_email
            subject = 'Lembrete de Pagamento'
            message = 'Lembramos que o Pagamento do seu pedido ainda está pendente. Por favor, realize o pagamento o mais breve possível.'
            send_mail(subject, message, remetente, [recipient_email])

        elif session['payment_status'] == 'canceled':
            pedido.status_pedido = 'Cancelado'
            # Notificar o cliente sobre o cancelamento do pedido
            remetente = config('EMAIL_HOST_USER')
            recipient_email = cliente_email
            subject = 'Cancelamento de Pedido'
            message = 'Infelizmente, o seu pedido foi cancelado. Entre em contato conosco para mais informações.'
            send_mail(subject, message, remetente, [recipient_email])

        # Salvar as alterações no pedido
        pedido.save()

    # except Pedidos.DoesNotExist:
    #     # Pedido não encontrado
    #     return Response(status=400, data={'error': 'Pedido não encontrado'})

    # except Exception as e:
    #     error_message = f"Erro ao lidar com o pagamento: {str(e)}"
    #     print(error_message)
    #     return Response(status=500, data={'error': error_message})


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
