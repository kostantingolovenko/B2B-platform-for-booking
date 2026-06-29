from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'organization', 'organization_name']
        read_only_fields = ['id', 'email', 'organization']