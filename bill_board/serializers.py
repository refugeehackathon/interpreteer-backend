from rest_framework import serializers

from user_management.utils import query_zip_code
from .models import Request, Offer
from user_management.models import Language
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
                  'direction_display', 'user',
                  'kind', 'kind_display', 'title', 'description', 'start_time',
                  'end_time', 'requires_presence', )

class OfferSerializer(serializers.ModelSerializer):
    kind_display = serializers.CharField(source='get_kind_display',
                                         read_only=True)
    distance = serializers.FloatField(
        read_only=True
    )

    class Meta:
        model = Offer
        fields = ('id', 'user',
                  'kind', 'kind_display', 'start_time',
                  'end_time', 'title', 'description', 'distance')
