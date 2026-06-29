from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InvoiceSerializer(many=True))
    def get(self, request):
        user = request.user

        if user.is_staff:
            invoices = Invoice.objects.all().order_by('-start_period')
        else:
            org = getattr(user, 'organization', None)
            if org:
                invoices = Invoice.objects.filter(organization=org).order_by('-start_period')
            else:
                invoices = Invoice.objects.none()  # Якщо немає організації, повертаємо пустий список

        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)


class InvoiceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InvoiceSerializer)
    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)

        if not request.user.is_staff:
            org = getattr(request.user, 'organization', None)
            if not org or invoice.organization != org:
                raise PermissionDenied("У вас немає прав для перегляду цього інвойсу.")

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)