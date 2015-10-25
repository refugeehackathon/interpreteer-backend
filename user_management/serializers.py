from rest_framework import serializers
from .models import UserProfile
from bill_board.serializers import LocationSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = UserProfile
        exclude = ('password', 'is_active', 'user_permissions', 'groups',
            'last_login', 'is_superuser', 'is_staff')
