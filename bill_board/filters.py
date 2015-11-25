import django_filters as df
from django.utils.dateparse import parse_datetime
from .models import Request, Offer, TYPE_CHOICES, DIRECTION_CHOICES


# TODO: Bring 'KnownLanguageRequestsFilter' and 'KnownLanguageOfferFilter' together
class KnownLanguageRequestsFilter(df.Filter):
    """
    Expects a comma separated list of language codes
    """
    def filter(self, qs, value):
        return qs.filter(known_languages__language_code__in=value.split(','))


class KnownLanguageOfferFilter(df.Filter):
    """
    Expects a comma separated list of language codes
    """
    def filter(self, qs, value):
        return qs.filter(
            user__translation_skills__source_language__language_code__in=value.split(',')
        )


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


class OffersFilter(df.FilterSet):
    """
    Filterset for Offers
    # TODO: location filter
    """
    kind = df.ChoiceFilter(choices=TYPE_CHOICES)
    time_range = TimeRangeFilter(within=True)
    required_language = df.CharFilter(
        name='user__translation_skills__destination_language__language_code'
    )
    known_languages = KnownLanguageOfferFilter()
    
    class Meta:
        model = Offer
        fields = ['kind', 'time_range', 'required_language', 'known_languages']


class RequestsFilter(df.FilterSet):
    """
    Filterset for requests
    # TODO: location filter
    """
    kind = df.ChoiceFilter(choices=TYPE_CHOICES)
    direction = df.ChoiceFilter(choices=DIRECTION_CHOICES)
    known_languages = KnownLanguageRequestsFilter()
    required_language = df.CharFilter(name='required_language__language_code')
    time_range = TimeRangeFilter(within=False)
    
    class Meta:
        model = Request
        fields = ['kind', 'direction', 'known_languages', 'required_language',
                  'time_range']