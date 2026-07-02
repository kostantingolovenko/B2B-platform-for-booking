from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'status', 'stripe_payment_intent_id', 'created_at')
    list_filter = ('status', 'stripe_payment_intent_id', 'created_at')
    search_fields = ('id', 'invoice__id', 'invoice__organization__name')
    readonly_fields = ('created_at', 'updated_at')