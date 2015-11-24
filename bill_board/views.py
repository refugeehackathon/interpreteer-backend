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
    def __init__(self, *args, **kwargs):
        self.within = kwargs.pop('within', True)
        df.Filter.__init__(self, *args, **kwargs)
    
    def filter(self, qs, value):
        begin, end = value.split(',')
        begin = parse_datetime(begin)
        end = parse_datetime(end)
        if self.within:
            qs = qs.filter(start_time__lte=begin, end_time__gte=end)
        else:
            qs = qs.filter(start_time__gte=begin, end_time__lte=end)
        return qs


class RequestsFilter(df.FilterSet):
    kind = df.ChoiceFilter(choices=TYPE_CHOICES)
    direction = df.ChoiceFilter(choices=DIRECTION_CHOICES)
    known_languages = KnownLanguageFilter()
    required_language = df.CharFilter(name='required_language__language_code')
    time_range = TimeRangeFilter(within=False)
    
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


class KnownLanguageOfferFilter(df.Filter):
    """
    Expects a comma separated list of language codes
    """
    def filter(self, qs, value):
        return qs.filter(user__translation_skills__source_language__language_code__in=value.split(','))


class OffersFilter(df.FilterSet):
    kind = df.ChoiceFilter(choices=TYPE_CHOICES)
    time_range = TimeRangeFilter(within=True)
    required_language = df.CharFilter(
        name='user__translation_skills__destination_language__language_code'
    )
    known_languages = KnownLanguageOfferFilter()
    
    class Meta:
        model = Offer
        fields = ['kind', 'time_range', 'required_language', 'known_languages']


class OffersViewset(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    # TODO: This should be move to settings
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OffersFilter

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        instance = serializer.save(user=self.request.user)
        return instance
