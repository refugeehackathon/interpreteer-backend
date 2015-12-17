""" Default urlconf for interpreteer """

from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework import routers
from bill_board.views import RequestsViewset, OffersViewset
from user_management.views import UserProfilesViewset, LanguagesViewset
admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'api/offers', OffersViewset)
router.register(r'api/requests', RequestsViewset)
router.register(r'api/users', UserProfilesViewset)
router.register(r'api/languages', LanguagesViewset)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^auth/', include('user_management.urls')),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
)

urlpatterns += router.urls
