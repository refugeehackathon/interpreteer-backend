from django.conf.urls import url, patterns
from . import views


urlpatterns = patterns(
    '',
    # the view to register our user with a third party token
    # the backend is the python social auth backend e.g. facebook
    url(r'register-by-token/(?P<backend>[^/]+)/$',
        views.register_by_access_token),
    url(r'login/$', views.login_by_password),
)
