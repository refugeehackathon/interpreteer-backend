from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework.viewsets import ModelViewSet
from social.apps.django_app.utils import psa

from .tools import get_access_token
from .serializers import UserProfileSerializer, LanguagesSerializer
from .models import UserProfile, Language


class UserProfilesViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class LanguagesViewset(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer


@csrf_exempt
def login_by_password(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return get_access_token(user)
        else:
            # TODO disabled account message
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


@psa('social:complete')
def register_by_access_token(request, backend):

    token = request.GET.get('access_token')
    # here comes the magic
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        # that function will return our own
        # OAuth2 token as JSON
        # Normally, we wouldn't necessarily return a new token, but you get the idea
        return get_access_token(user)
    else:
        # If there was an error... you decide what you do here
        return HttpResponse("error")
