# from django.shortcuts import redirect
# import stripe
# import json
# import os
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from decouple import config


# # This is your test secret API key.
# stripe_secret_key = config('STRIPE_SECRET_KEY')
# if not stripe_secret_key:
#     raise ValueError('A chave secreta do Stripe não está definida no ambiente.')



# def create_checkout_session(request):
#     try:
       
#         # sacola = json.loads(b'')
#         sacola = [
#             {
#                 "price_data": {
#                     "currency": "brl",
#                     "unit_amount": 100,
#                     "product_data": {
#                         "name": "Produto 1"
#                     }
#                 },
#                 "quantity": 2
#             },
#             {
#                 "price_data": {
#                     "currency": "brl",
#                     "unit_amount": 200,
#                     "product_data": {
#                         "name": "Produto 2"
#                     }
#                 },
#                 "quantity": 1
#             }
#         ]

        
#         # for item in sacola:
            
#         #     line_item = {
#         #         'price_data': {
#         #             'currency': 'brl',
#         #             'unit_amount': int(item['price_data']['unit_amount']) * 100,
#         #             'product_data': {
#         #                 'name': item['price_data']['product_data']['name'],
#         #             },
#         #         },
#         #         'quantity': item['quantity'],
#         #     }
#         #     line_items.append(line_item)

#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=sacola,
#             mode='payment',
#             success_url='/success.html',
#             cancel_url='/cancel.html',
#         )
#         print(checkout_session)
#     except Exception as e:
#         print(e)
#         return str(e)

#     return redirect(checkout_session.url, code=303)

# # @csrf_exempt
# # def create_checkout_session(request):
# #     # Criar uma lista de itens de linha fictícios
# #     # Receber os dados enviados no corpo da solicitação POST
# #     sacola = json.loads(request.body)

# #     line_items = []
# #     for item in sacola:

# #         line_item = {
# #             'price_data': {
# #                 'currency': 'brl',
# #                 'unit_amount': int(item['price_data']['unit_amount']) * 100,
# #                 'product_data': {
# #                     'name': item['price_data']['product_data']['name'],
# #                 },
# #             },
# #             'quantity': item['quantity'],
# #         }
# #         line_items.append(line_item)

# #     session = stripe.checkout.Session.create(
# #         payment_method_types=['card'],
# #         line_items=line_items,
# #         mode='payment',
# #         success_url='https://seusite.com.br/success/',
# #         cancel_url='http://localhost:9000/cliente/visao-geral/',
# #     )

# #     return JsonResponse({'session_id': session.id})
