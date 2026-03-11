# test.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

from django.conf import settings
print(f"SETTINGS_MODULE: {settings.SETTINGS_MODULE}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")