from decimal import Decimal
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'desk', 'start_time', 'end_time', 'status', 'total_price']
        read_only_fields = ['user', 'total_price', 'status']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')
        desk = data.get('desk')

        if start >= end:
            raise ValueError({"end_time": "Час завершення має бути пізніше початку."})

        overlaying = Booking.objects.filter(
            desk=desk,
            start_time__lt=end,
            end_time__gt=start
        )

        if self.instance:
            overlaying = overlaying.exclude(id=self.instance.id)

        if overlaying.exists():
            raise serializers.ValidationError({"desk": "Цей стіл вже заброньовано на цей час."})

        return data

    def create(self, validated_data):
        duration = validated_data.get('end_time') - validated_data.get('start_time')
        hours = duration.total_seconds() / 3600
        validated_data['total_price'] = round(validated_data.get('desk').
                                              price_per_hour * Decimal(str(hours)), 2)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)