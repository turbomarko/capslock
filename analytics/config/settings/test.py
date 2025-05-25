"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="WwNaDAypr7pKHzAbFaRW1on91iIqiYXTekE8ak33lCxU499x21lIWOEsg26uHfOa",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"
