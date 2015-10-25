""" Settings for interpreteer """

from .base import *
import os
try:
    if "heroku" in os.environ.get('DJANGO_SETTINGS_MODULE'):
        from .heroku import *
    else:
        from .local import *
except ImportError as exc:
    exc.args = tuple(
        ['%s (did you rename settings/local-dist.py?)' % exc.args[0]])
    raise exc
