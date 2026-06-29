from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, OfficeViewSet, RoomViewSet, DeskViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'offices', OfficeViewSet, basename='office')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'desks', DeskViewSet, basename='desk')

urlpatterns = [
    path('', include(router.urls))
]