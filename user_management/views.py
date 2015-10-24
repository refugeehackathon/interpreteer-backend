from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from .models import UserProfile


class UserProfilesViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
