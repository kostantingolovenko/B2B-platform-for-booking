from django.urls import path
from .views import BookingDetailAPIView, BookingListCreateAPIView, OfficeOccupancyAPIView

urlpatterns = [
    path('/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail-update-delete'),
    path('analytics/occupancy/', OfficeOccupancyAPIView.as_view(), name='office-occupancy')
]
