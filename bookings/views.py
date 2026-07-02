from datetime import timedelta
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from .models import Booking
from spaces.models import Office, Desk
from .serializers import BookingSerializer
from .permissions import IsOwnerOrAdmin

class BookingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=BookingSerializer(many=True))
    def get(self, request):
        query_set = Booking.objects.select_related('user','user__organization', 'desk', 'desk__room')
        if request.user.is_staff:
            bookings = (query_set
                        .filter(user__organization=getattr(request.user, 'organization', None))
                        .order_by('-start_time'))
        else:
            bookings = query_set.filter(user=request.user).order_by('-start_time')

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(bookings, request)

        serializer = BookingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=BookingSerializer, responses={201: BookingSerializer})
    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @extend_schema(responses=BookingSerializer)
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def put(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={204: None})
    def delete(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)
        booking.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OfficeOccupancyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: dict})
    def get(self, request):
        user = request.user
        org = getattr(user, 'organization', None)

        if not org:
            return Response({"error": "Користувач не належить до організації"}, status=400)

        end_time = timezone.now()
        start_time = end_time - timedelta(days=7)

        offices = Office.objects.filter(organization=org, is_active=True)
        offices_count = offices.count()

        if offices_count == 0:
            return Response({"message": "В організації немає активних просторів",
                "occupancy_percentage": 0})

        total_available_hours = 0
        for office in offices:
            open_h = office.open_time.hour + (office.open_time.minute / 60)
            close_h = office.close_time.hour + (office.close_time.minute / 60)
            daily_office_hours = close_h - open_h

            desks_count = Desk.objects.filter(
                room__office=office,
                is_active=True,
                room__is_active=True
            ).count()

            total_available_hours += daily_office_hours * 7 * desks_count

        bookings = Booking.objects.filter(
            desk__room__office__in=offices,
            start_time__gte=start_time,
            start_time__lt=end_time
        )

        duration_data = bookings.aggregate(
            total_duration=Sum(
                ExpressionWrapper(
                    F('end_time') - F('start_time'),
                    output_field=DurationField()
                )
            )
        )
        total_duration = duration_data['total_duration']

        booked_hours = 0
        if total_duration:
            booked_hours = total_duration.total_seconds() / 3600

        if total_available_hours > 0:
            occupancy_percentage = (booked_hours / total_available_hours) * 100
        else:
            occupancy_percentage = 0

        return Response(
            {
                "period": {
                    "start": start_time,
                    "end": end_time
                },
                "offices_count": offices_count,
                "total_available_hours": round(total_available_hours, 2),
                "booked_hours": round(booked_hours, 2),
                "occupancy_percentage": round(occupancy_percentage, 2)
            }
        )
