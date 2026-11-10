"""
Passenger WSGI configuration for cPanel / CloudLinux (Namecheap Stellar Plus).
This file serves as the entry point for Phusion Passenger.
"""

import os
import sys

# Add project root directory to the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getnexiro.settings')

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
