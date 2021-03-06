from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer, LanguagesSerializer, LocationSerializer
from .models import UserProfile, Language, Location

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class UserProfilesViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class LanguagesViewset(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer

class LocationsViewset(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
