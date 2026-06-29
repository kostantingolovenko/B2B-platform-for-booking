from django.urls import path
from .views import BookingDetailAPIView, BookingListCreateAPIView

urlpatterns = [
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('booking/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail-update-delete')
]
