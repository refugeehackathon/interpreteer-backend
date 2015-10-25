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
    kind_display = serializers.CharField(source='get_kind_display',
                                         read_only=True)
    direction_display = serializers.CharField(source='get_direction_display',
                                              read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'required_language', 'known_languages', 'direction',
                  'direction_display', 'user', 'location',
                  'kind', 'kind_display', 'title', 'description', 'start_time',
                  'duration', 'requires_presence', )

    def create_location(self, validated_data):
        return Location.objects.create(**validated_data)

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = self.create_location(location_data)
        validated_data['location_id'] = location.id
        # TODO: get from logged in user
        # validated_data['user_id'] = 1
        return serializers.ModelSerializer.create(self, validated_data)

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    location = LocationSerializer()
    kind_display = serializers.CharField(source='get_kind_display',
                                         read_only=True)
    class Meta:
        model = Request
        fields = ('id', 'user', 'location',
                  'kind', 'kind_display', 'start_time',
                  'duration', )

    def create_location(self, validated_data):
        return Location.objects.create(**validated_data)

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = self.create_location(location_data)
        validated_data['location_id'] = location.id
        # TODO: get from logged in user
        # validated_data['user_id'] = 1
        return serializers.ModelSerializer.create(self, validated_data)
