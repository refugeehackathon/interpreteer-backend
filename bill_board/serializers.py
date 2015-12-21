from rest_framework import serializers

from user_management.utils import query_zip_code
from .models import Request, Offer
from user_management.models import Language, Location
from user_management.serializers import LocationSerializer


class RequestSerializer(serializers.ModelSerializer):
    required_language = serializers.SlugRelatedField(
        slug_field='language_code', queryset=Language.objects.all()
    )
    known_languages = serializers.SlugRelatedField(
        slug_field='language_code', queryset=Language.objects.all(), many=True
    )
    kind_display = serializers.CharField(source='get_kind_display',
                                         read_only=True)
    direction_display = serializers.CharField(source='get_direction_display',
                                              read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'required_language', 'known_languages', 'direction',
                  'direction_display', 'user', 'location',
                  'kind', 'kind_display', 'title', 'description', 'start_time',
                  'end_time', 'requires_presence', )

    def create_location(self, validated_data):
        if validated_data["location"] is None:
            validated_data["location"] = query_zip_code(validated_data["zip_code"])
        return Location.objects.create(**validated_data)

    def create(self, validated_data):
        # TODO: get from logged in user
        # validated_data['user_id'] = 1
        return serializers.ModelSerializer.create(self, validated_data)

class OfferSerializer(serializers.ModelSerializer):
    kind_display = serializers.CharField(source='get_kind_display',
                                         read_only=True)
    class Meta:
        model = Offer
        fields = ('id', 'user', 'location',
                  'kind', 'kind_display', 'start_time',
                  'end_time', 'title', 'description',)

    def create_location(self, validated_data):
        return Location.objects.create(**validated_data)

    def create(self, validated_data):
        # TODO: get from logged in user
        # validated_data['user_id'] = 1
        return serializers.ModelSerializer.create(self, validated_data)
