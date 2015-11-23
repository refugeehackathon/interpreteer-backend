from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import RequestSerializer, OfferSerializer
from .models import Request, Offer, TYPE_CHOICES, DIRECTION_CHOICES
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotAuthenticated
import datetime
import django_filters as df
from rest_framework import filters
from django.utils.dateparse import parse_datetime


class KnownLanguageFilter(df.Filter):
    """
    Expects a comma separated list of language codes
    """
    def filter(self, qs, value):
        return qs.filter(known_languages__language_code__in=value.split(','))


class TimeRangeFilter(df.Filter):
    """
    Expects a comma separated list of iso-8601 datetime
    """        
    def filter(self, qs, value):
        begin, end = value.split(',')
        begin = parse_datetime(begin)
        end = parse_datetime(end)
        qs = qs.filter(start_time__gte=begin, end_time__lte=end)
        return qs


class RequestsFilter(df.FilterSet):
    kind = df.ChoiceFilter(choices=TYPE_CHOICES)
    direction = df.ChoiceFilter(choices=DIRECTION_CHOICES)
    known_languages = KnownLanguageFilter()
    required_language = df.CharFilter(name='required_language__language_code')
    time_range = TimeRangeFilter()
    
    class Meta:
        model = Request
        fields = ['kind', 'direction', 'known_languages', 'required_language',
                  'time_range']


class RequestsViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    # TODO: This should be move to settings
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RequestsFilter
    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        instance = serializer.save(user=self.request.user)
        return instance

    @detail_route(['GET'])
    def matchings(self, request, pk):
        obj = self.get_object()
        matchings = obj.matching_offers()
        return Response(OfferSerializer(matchings, many=True).data)


class OffersViewset(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        instance = serializer.save(user=self.request.user)
        return instance
