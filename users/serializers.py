from rest_framework import serializers
from django.contrib.auth import get_user_model
from spaces.models import Organization  # Переконайся, що імпорт правильний для твого проєкту

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'organization', 'organization_name']
        read_only_fields = ['id', 'email', 'organization']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        # Використовуємо create_user для автоматичного хешування пароля
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
        )
        return user


class AssignOrganizationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    organization_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Користувача з таким ID не знайдено.")
        return value

    def validate_organization_id(self, value):
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Організацію з таким ID не знайдено.")
        return value