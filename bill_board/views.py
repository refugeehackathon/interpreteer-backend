from rest_framework.viewsets import ModelViewSet
from .serializers import RequestSerializer
from .models import Request


class RequestsViewset(ModelViewSet):
    
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        '''
        Set User as creator
        '''
        instance = serializer.save(user=self.request.user)
        return instance