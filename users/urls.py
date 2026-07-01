from django.urls import path
from .views import UserProfileAPIView, UserRegistrationAPIView, AssignOrganizationAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('assign-organization/', AssignOrganizationAPIView.as_view(), name='assign-organization'),
]