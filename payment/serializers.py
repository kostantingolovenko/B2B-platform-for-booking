from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['invoice', 'amount', 'status', 'stripe_payment_intent_id', 'created_at', 'updated_at']
        read_only_fields = ['invoice', 'amount', 'status', 'stripe_payment_intent_id', 'created_at', 'updated_at']

class CheckoutSessionRequestSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()

