import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = 'sk_test_51MPlr3BEkVZTqnMr5tdzee7gecC4LE0HfmfA5IcsuS8gskSVZGYZtVSv28DA30U8CGQ47tF8pIJNuKfZQatps7F1007ytjdio7'

@csrf_exempt
def create_checkout_session(request):
    # Criar uma lista de itens de linha fictícios
    # Receber os dados enviados no corpo da solicitação POST
    sacola = json.loads(request.body)

    line_items = []
    for item in sacola:

        line_item = {
            'price_data': {
                'currency': 'brl',
                'unit_amount': int(item['price_data']['unit_amount']) * 100,
                'product_data': {
                    'name': item['price_data']['product_data']['name'],

                },
            },
            'quantity': item['quantity'],
        }
        line_items.append(line_item)

    session = stripe.checkout.Session.create(
        submit_type='pay',
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:9000/cliente/sucesso/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://localhost:9000/cliente/visao-geral/',
        
    )

    return JsonResponse({'session_id': session.id})



