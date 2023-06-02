from django.contrib import admin

from ..models import Stripe


@admin.register(Stripe)
class StripeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'webhook'
    ]

    search_fields = [
        'id',
        'webhook'
    ]

    list_filter = [
        
    ]

   
