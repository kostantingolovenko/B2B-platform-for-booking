from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'organization',
            'organization_name',
            'status',
            'status_display',
            'start_period',
            'end_period',
            'total_amount'
        ]