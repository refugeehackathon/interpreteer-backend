import django_filters as df
from rest_framework import filters
from django.utils.dateparse import parse_datetime
from .models import Request, Offer, TYPE_CHOICES, DIRECTION_CHOICES

from django.contrib.gis.geos import Point

from django.db.backends.signals import connection_created
from django.dispatch import receiver

import math

# TODO: Move somewhere else or abandon SQLite altogether
@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)


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

class DistanceFilter(filters.BaseFilterBackend):
    dist_param = 'dist'
    point_param = 'point'

    def get_filter_point(self, request):
        point_string = request.query_params.get(self.point_param, None)
        if not point_string:
            return None

        try:
            (x, y) = (float(n) for n in point_string.split(','))
        except ValueError:
            raise ParseError('Invalid geometry string supplied for parameter {0}'.format(self.point_param))

        p = Point(x, y)
        return p

    def filter_queryset(self, request, queryset, view):
        convert_distance_input = getattr(view, 'distance_filter_convert_meters', False)

        dist_string = request.query_params.get(self.dist_param, 5000)
        if not dist_string:
            return queryset

        point = self.get_filter_point(request)
        if not point:
            return queryset

        try:
            dist = float(dist_string)
        except ValueError:
            raise ParseError('Invalid distance string supplied for parameter {0}'.format(self.dist_param))

        gcd = """
              6371.0 * acos(
               cos(radians(%s)) * cos(radians("user_management_location"."latitude"))
               * cos(radians("user_management_location"."longitude") - radians(%s)) +
               sin(radians(%s)) * sin(radians("user_management_location"."latitude"))
              )
              """
        gcd_lt = '{} < %s'.format(gcd)
        return queryset.select_related('user__location')\
            .exclude(user__location__latitude=None)\
            .exclude(user__location__longitude=None)\
            .extra(
               select={'distance': gcd},
               select_params=[point.x, point.y, point.x],
               where=[gcd_lt],
               params=[point.x, point.y, point.x, dist],
               order_by=['distance']
            )

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
