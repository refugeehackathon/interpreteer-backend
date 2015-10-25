from rest_framework.viewsets import ModelViewSet
from .serializers import RequestSerializer, OfferSerializer
from .models import Request, Offer


class RequestsViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        '''
        Set User as creator
        '''
        # set fake user:
        instance = serializer.save(user_id=1)
        #instance = serializer.save(user=self.request.user)
        return instance

class OffersViewset(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        '''
        Set User as creator
        '''
        # set fake user:
        instance = serializer.save(user_id=2)
        #instance = serializer.save(user=self.request.us.user)
        return instance
