from rest_framework import serializers
from .models import Organization, Office, Room, Desk

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'email', 'website']

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['id', 'organization', 'name', 'city', 'address', 'open_time', 'close_time', 'phone']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'office', 'name', 'floor', 'room_type', 'capacity', 'has_projector'
            , 'has_whiteboard']

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['id', 'room', 'number', 'is_adjustable', 'price_per_hour']