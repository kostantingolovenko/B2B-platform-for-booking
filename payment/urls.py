from django.urls import path
from .views import CreateStripeCheckoutAPIView, StripeWebhookAPIView, PaymentListAPIView, PaymentDetailAPIView

urlpatterns = [
    path('create-checkout-session/', CreateStripeCheckoutAPIView.as_view(), name='create-checkout-session'),
    path('webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'),
    path('', PaymentListAPIView.as_view(), name='payment-list'),
    path('<int:pk>', PaymentDetailAPIView.as_view(), name='payment-detail')
]