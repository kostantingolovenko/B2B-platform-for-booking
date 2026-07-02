from django.urls import path
from .views import CreateStripeCheckoutAPIView, StripeWebhookAPIView

urlpatterns = [
    path('create-checkout-session/', CreateStripeCheckoutAPIView.as_view(), name='create-checkout-session'),
    path('webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'),
]