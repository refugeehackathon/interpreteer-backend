from rest_framework import serializers
from .models import UserProfile, LanguageSkill
from bill_board.serializers import LocationSerializer


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(slug_field='language_code',
                                            read_only=True) 
    class Meta: 
        model = LanguageSkill
        fields = ('language', 'level')

class UserProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    language_skills = LanguageSkillSerializer(many=True)

    class Meta:
        model = UserProfile
        exclude = ('password', 'is_active', 'user_permissions', 'groups',
            'last_login', 'is_superuser', 'is_staff', 'first_name',
            'last_name')
