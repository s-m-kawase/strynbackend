import stripe
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from pedidos.models import Pedidos
from pagamentos.models import Pagamento
from decouple import config
from emails.models import MensagemEmail, TemplateEmail
from collections import namedtuple
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.core import serializers
asaas_api = config('ASAAS_API_KEY')

class AsaasWebhookViewSet(ViewSet):

    def cobranca_criada(self, pedido, email):
        try:
            template_email = TemplateEmail.objects.filter(
                codigo='criar_cobranca'
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


    def update_pedido_status(self, pedido, email):
        
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
        

    def estorno(self, pedido, email):
        pedido.status_pedido == 'Cancelado'
        pedido.save()
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
        

         

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def webhook(self, request):
        
        payload = request.data

        event_type = payload.get('event')

        if event_type == 'PAYMENT_CREATED':
            payment_data = payload['payment']
            ped = payment_data['externalReference']
            pedido = Pedidos.objects.get(id=ped)  
            pedido_data = serializers.serialize('json', [pedido])  
            # return JsonResponse({
            #     "payment_data":payment_data['externalReference'],
            #     "pedido":pedido_data,
            #                                 })
            
            email = pedido.email_cliente
            pedido.pagamento_asaas = payment_data['id']
            pedido.save()
            try:
                template_email = TemplateEmail.objects.filter(
                    codigo='criar_cobranca'
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
            # self.cobranca_criada(pedido, email)

        if event_type == 'PAYMENT_RECEIVED':
            payment_data = payload['payment']
            pedido_id = payment_data['externalReference']
            pedido = Pedidos.objects.get(id=pedido_id)
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

            except Exception as error:
                return JsonResponse(
                    {
                        "status": "404",
                        "message": error.args[0],
                    }
                )
            Pagamento.objects.create(
            pedido=pedido,
            pagamento="Pagamento pix",
            valor_pago=pedido.total,
            codigo_pagamento=f"PIX{pedido}"
            )

        if event_type == 'PAYMENT_REFUNDED':
            payment_data = payload['payment']
            pedido_id = payment_data['externalReference']
            pedido = Pedidos.objects.get(id=pedido_id)
            email = pedido.email_cliente
            pedido.status_pedido == 'Cancelado'
            pedido.save()
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
        

            # self.estorno(pedido, email)
            
                

        return JsonResponse({'message': 'Webhook recebido com sucesso'})
