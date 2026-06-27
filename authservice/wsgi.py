import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authservice.settings")

application = get_wsgi_application()

try:
    from labora_shared.env_config import validate_mysql_connection_readable
except ImportError:
    pass
else:
    validate_mysql_connection_readable()
