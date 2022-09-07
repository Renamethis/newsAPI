from __future__ import absolute_import, unicode_literals
import sys, locale
from .celery import app as celery_app
# Set locale for Russian datetime support
if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
__all__ = ('celery_app',)