import sys
import os

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG = True,
    SECRET_KEY = 'holaaanadiedeberiaenterarsedeesto:)',
    ROOT_URLCONF = 'sitebuilder.urls',
    MIDDLEWARE_CLASSES = (),
    INSTALLED_APPS = (
        'django.contrib.staticfiles',
        'django.contrib.webdesign', #en django 1.8 solo nos habilita {% lorem %}
        'sitebuilder'
    ),
    STATIC_URL = '/static/',
    SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR, 'pages'),
    SITE_OUTPUT_DIRECTORY = os.path.join(BASE_DIR,'_build'),
    STATIC_ROOT = os.path.join(BASE_DIR, '_build','static'),
)


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)