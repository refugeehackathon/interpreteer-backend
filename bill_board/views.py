from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import RequestSerializer, OfferSerializer
from .models import Request, Offer
from .filters import RequestsFilter, OffersFilter, DistanceFilter
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotAuthenticated
from rest_framework import filters


class RequestsViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    # TODO: This should be move to settings
    filter_backends = (filters.DjangoFilterBackend, DistanceFilter)
    filter_fields = ('location',)
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
    # TODO: This should be move to settings
    filter_backends = (filters.DjangoFilterBackend, DistanceFilter)
    filter_fields = ('location',)
    filter_class = OffersFilter

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        instance = serializer.save(user=self.request.user)
        return instance
