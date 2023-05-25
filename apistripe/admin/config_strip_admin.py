from django.contrib import admin

from ..models import ConfigStripe


@admin.register(ConfigStripe)
class ConfigStripeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome'
    ]

    search_fields = [
        'id',
        'nome'
    ]

    list_filter = [
        'nome'
    ]
