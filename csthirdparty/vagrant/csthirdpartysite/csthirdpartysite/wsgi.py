import os
import sys
from django.core.wsgi import get_wsgi_application

"""
WSGI config for coffeeshopsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "../")))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csthirdpartysite.settings')

application = get_wsgi_application()
