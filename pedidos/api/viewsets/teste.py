import requests
from django.conf import settings
from ...models import Pedidos  

def registrar_pagamento_pix(valor, descricao, chave_pix, pedido_id):
    url = "https://sandbox.asaas.com/api/v3/payments"
    # Gere um payload Pix para a solicitação de pagamento
    payload = {
        "valor": valor,
        "descricao": descricao,
        "chave_pix": chave_pix,
    }

    # Faça uma solicitação ao seu provedor de pagamento Pix para iniciar a transação
    response_pix = requests.post("URL_DO_SEU_SERVICO_PIX", json=payload)

    if response_pix.status_code == 200:
        # O pagamento via Pix foi bem-sucedido, registre a transação no Asaas
        response_data = response_pix.json()
        
        # Registre a transação no modelo Pedido
        pedido = Pedidos.objects.get(id=pedido_id)
        pedido.status_pagamento = "PAGO"
        pedido.referencia_pix = response_data["referencia"]
        pedido.save()

        # Agora, você pode registrar a transação no Asaas usando a API do Asaas
        registrar_transacao_asaas(pedido)

        return True
    else:
        # Lidar com erros no pagamento via Pix
        return False

def registrar_transacao_asaas(pedido):
    # Use a API do Asaas para criar uma transação no Asaas
    url = "https://www.asaas.com/api/v3/payments"

    payload = {
        "customer": pedido.cliente_id,  # Suponha que você tenha o ID do cliente associado ao pedido
        "billingType": "PIX",
        "value": pedido.valor_total,
        "description": pedido.descricao,
    }

    headers = {
        "access_token": settings.ASAAS_API_KEY,
        "secret_key": settings.ASAAS_API_SECRET,
        "Content-Type": "application/json",
    }

    response_asaas = requests.post(url, json=payload, headers=headers)

    if response_asaas.status_code == 200:
        # O pagamento foi registrado com sucesso no Asaas
        # Atualize o status da transação no modelo Pedido, se necessário
        pedido.status_asaas = "CONCLUIDO"
        pedido.save()
    else:
        # Lidar com erros no registro da transação no Asaas
        pass
