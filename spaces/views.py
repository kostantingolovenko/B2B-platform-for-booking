from rest_framework import viewsets

from .models import Organization, Office, Room, Desk
from .serializers import OrganizationSerializer, OfficeSerializer, RoomSerializer, DeskSerializer
from .permissions import IsAdminOrReadOnly

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by('name')
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ['name']

class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by('name')
    serializer_class = OfficeSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ['name', 'organization', 'city', 'address', 'open_time', 'close_time']

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ['office', 'name', 'floor', 'room_type', 'capacity', 'has_projector',
                        'has_whiteboard']

class DeskViewSet(viewsets.ModelViewSet):
    queryset = Desk.objects.all().order_by('number')
    serializer_class = DeskSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ['room', 'number', 'is_adjustable', 'price_per_hour']