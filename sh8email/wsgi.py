"""
WSGI config for sh8email project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# If we use WSGI, then may it will be the situtation should load production settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sh8email.settings_prod")

application = get_wsgi_application()
