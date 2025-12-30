import os
import sys
import django
from django.core.mail import send_mail

# Ensure project root is on sys.path (so 'backend' package is importable)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

# Configure Django settings for standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


from django.conf import settings

print('DEFAULT_FROM_EMAIL=', getattr(settings, 'DEFAULT_FROM_EMAIL', None))
print('SUPPORT_EMAIL=', getattr(settings, 'SUPPORT_EMAIL', None))

from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'no-reply@example.org'
to_email = getattr(settings, 'SUPPORT_EMAIL', None) or from_email

print('Sending test email from', from_email, 'to', to_email)
res = send_mail('BCMRV test email', 'This is an automated test from the BlueQuant project.', from_email, [to_email], fail_silently=False)
print('send_mail returned', res)
