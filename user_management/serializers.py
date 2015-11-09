from rest_framework import serializers
from .models import UserProfile, LanguageSkill, Language, Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location

class LanguagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language

class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(
        slug_field='language_code', read_only=True
    )

    class Meta:
        model = LanguageSkill
        fields = ('id', 'language', 'level')

class UserProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    language_skills = LanguageSkillSerializer(many=True)

    class Meta:
        model = UserProfile
        exclude = ('password', 'is_active', 'user_permissions', 'groups',
            'last_login', 'is_superuser', 'is_staff', 'first_name',
            'last_name')

    def update(self, instance, validated_data):
        language_data = validated_data.pop('language_skills')
        if language_data:
            # add /update languages
            active_languages = []
            for lang in language_data:
                active_languages.append(lang['language'])
                obj, created = LanguageSkill.objects.get_or_create(
                    language=lang['language'], user=instance
                )
                obj.level = lang['level']
                obj.save()
            # remove deleted languages
            instance.language_skills.exclude(language__in=active_languages).delete()

        location_data = validated_data.pop('location')
        if location_data:
            # TODO: change location data
            instance.location.zip_code = location_data['zip_code']
            pass
        return serializers.ModelSerializer.update(self, instance, validated_data)
