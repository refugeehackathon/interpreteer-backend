from rest_framework import serializers
from .models import Request
from user_management.models import Language, Location


class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        exclude = ('id',)


class RequestSerializer(serializers.ModelSerializer):
    required_language = serializers.SlugRelatedField(
        slug_field='language_code', queryset=Language.objects.all()
    )
    known_languages = serializers.SlugRelatedField(
        slug_field='language_code', queryset=Language.objects.all(), many=True
    )
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    location = LocationSerializer()
    kind_display = serializers.CharField(source='get_kind_display')
    direction_display = serializers.CharField(source='get_direction_display')
    
    class Meta:
        model = Request
        fields = ('required_language', 'known_languages', 'direction', 
                  'direction_display', 'user', 'location',
                  'kind', 'kind_display', 'title', 'description', 'start_time',
                  'duration', 'requires_presence', )