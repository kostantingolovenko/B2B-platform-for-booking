import stripe
from django.db.migrations import serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404

from invoice.models import Invoice
from users.models import User
from .models import Payment
from .serializers import PaymentSerializer, CheckoutSessionRequestSerializer
from django.conf import settings
from .permissions import IsAdminAndInOrganization

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CheckoutSessionRequestSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = CheckoutSessionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        invoice_id = serializer.validated_data['invoice_id']
        invoice = get_object_or_404(Invoice, id=invoice_id, organization=request.user.organization)

        if invoice.status == 'successful':
            return Response({'detail': 'Цей рахунок вже оплачено.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'sepa_debit'],
                line_items=[{
                    'price_data': {
                        'currency': 'uah',
                        'unit_amount': int(invoice.total_amount * 100),
                        'product_data': {
                            'name': f'Оплата рахунку #{invoice.id}',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
                metadata={'invoice_id': invoice.id}
            )
            return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StripeWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', 'whsec_...')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return Response({"detail": "Невалідні дані"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response({"detail": "Невалідний криптографічний підпис"}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            invoice_id = session['metadata'].get('invoice_id')

            if invoice_id:
                invoice = Invoice.objects.get(id=invoice_id)
                invoice.status = 'paid'
                invoice.save()

                Payment.objects.create(
                    invoice=invoice,
                    amount=invoice.total_amount,
                    status='successful',
                    stripe_payment_intent_id=session.get('payment_intent')  # корисно для рефандів
                )
                print(f"Рахунок {invoice_id} успішно оплачено та збережено в Payment!")

        return Response(status=status.HTTP_200_OK)

class PaymentListAPIView(APIView):
    permission_classes = [IsAdminAndInOrganization]

    @extend_schema(responses=PaymentSerializer(many=True))
    def get(self, request):
        payments = Payment.objects.filter(invoice__organization=request.user.organization).select_related('invoice').order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

class PaymentDetailAPIView(APIView):
    permission_classes = [IsAdminAndInOrganization]

    @extend_schema(responses=PaymentSerializer)
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk, invoice__organization=request.user.organization)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

