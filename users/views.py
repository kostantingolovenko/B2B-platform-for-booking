from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from spaces.models import Organization
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    AssignOrganizationSerializer
)

User = get_user_model()


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=UserRegistrationSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignOrganizationAPIView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(request=AssignOrganizationSerializer, responses={200: UserSerializer})
    def post(self, request):
        serializer = AssignOrganizationSerializer(data=request.data)

        if serializer.is_valid():
            target_org_id = serializer.validated_data['organization_id']

            if request.user.organization_id != target_org_id:
                return Response(
                    {"detail": "Ви можете додавати користувачів лише до своєї організації."},
                    status=status.HTTP_403_FORBIDDEN
                )

            user_id = serializer.validated_data['user_id']
            user = get_object_or_404(User, id=user_id)

            user.organization_id = target_org_id
            user.save()

            response_serializer = UserSerializer(user)
            return Response(
                {"message": "Користувача успішно додано до організації.", "user": response_serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)