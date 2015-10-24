from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from .models import UserProfile

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class UserProfilesViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
