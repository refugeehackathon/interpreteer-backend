""" Default urlconf for interpreteer """

from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework import routers
from bill_board.views import RequestsViewset
from user_management.views import UserProfilesViewset
admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'bill-board/requests', RequestsViewset)
router.register(r'user_management/users', UserProfilesViewset)

def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'interpreteer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bad/$', bad),
    url(r'', include('base.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

)

urlpatterns += router.urls
