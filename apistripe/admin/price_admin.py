from django.contrib import admin

from ..models import Price


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'produto',
        'stripe_price_id',
        'price'
    ]

    search_fields = [
        'id',
        'produto',
    ]

    list_filter = [
        'produto'
    ]

    autocomplete_fields = [
        'produto'
    ]
