from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsOwnerOrAdmin

class BookingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=BookingSerializer(many=True))
    def get(self, request):
        if request.user.is_staff:
            bookings = Booking.objects.all().order_by('-start_time')
        else:
            bookings = Booking.objects.all().filter(user=request.user).order_by('-start_time')

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
