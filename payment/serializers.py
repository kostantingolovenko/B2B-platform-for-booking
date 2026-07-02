from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    invoice_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = ['invoice', 'amount', 'status', 'stripe_payment_intent_id', 'invoice_id']

class CheckoutSessionRequestSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()


