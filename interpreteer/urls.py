""" Default urlconf for interpreteer """

from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework import routers
from bill_board.views import RequestsViewset, OffersViewset
from user_management.views import UserProfilesViewset, FacebookLogin
admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'api/offers', OffersViewset)
router.register(r'api/requests', RequestsViewset)
router.register(r'api/users', UserProfilesViewset)

def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('',
    # Examples:
    url(r'', include('base.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bad/$', bad),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),

)

urlpatterns += router.urls
