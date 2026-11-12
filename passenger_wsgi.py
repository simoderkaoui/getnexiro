import os
import sys
import glob

# Current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Auto-detect project root: check if manage.py is in CURRENT_DIR or in a nested getnexiro/ folder
if os.path.exists(os.path.join(CURRENT_DIR, "manage.py")):
    PROJECT_DIR = CURRENT_DIR
elif os.path.exists(os.path.join(CURRENT_DIR, "getnexiro", "manage.py")):
    PROJECT_DIR = os.path.join(CURRENT_DIR, "getnexiro")
else:
    PROJECT_DIR = CURRENT_DIR

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Auto-detect cPanel virtualenv site-packages (Python 3.12, 3.11, etc.)
home = os.path.expanduser("~")
venv_patterns = [
    os.path.join(home, "virtualenv", "getnexiro", "*", "lib", "python*", "site-packages"),
    os.path.join(home, "virtualenv", "*", "*", "lib", "python*", "site-packages"),
    os.path.join(home, ".virtualenvs", "*", "lib", "python*", "site-packages"),
]

for pattern in venv_patterns:
    for sp in glob.glob(pattern):
        if sp not in sys.path:
            sys.path.insert(0, sp)

# Set Django settings module (guard against stale cPanel 'config' environment variable)
if os.environ.get('DJANGO_SETTINGS_MODULE') in (None, '', 'config', 'config.settings'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'getnexiro.settings'
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getnexiro.settings')

# Wrap WSGI loading to capture startup errors cleanly and repair cPanel Apache WSGI environ
try:
    from django.core.wsgi import get_wsgi_application
    _django_app = get_wsgi_application()

    def application(environ, start_response):
        # Fix for Apache mod_passenger on cPanel:
        # When request URI has Arabic / non-ASCII characters, Apache incorrectly
        # populates SCRIPT_NAME with the matched path, breaking Django's reverse()
        # and url resolver. Reset SCRIPT_NAME to '' and extract full path from REQUEST_URI.
        request_uri = environ.get('REQUEST_URI', '')
        if request_uri:
            full_path = request_uri.split('?')[0]
        else:
            full_path = environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', '')

        environ['SCRIPT_NAME'] = ''
        environ['PATH_INFO'] = full_path

        return _django_app(environ, start_response)
except Exception:
    import traceback
    error_trace = traceback.format_exc()

    # Save traceback to file for diagnosis
    try:
        with open(os.path.join(CURRENT_DIR, "passenger_error.log"), "w", encoding="utf-8") as f:
            f.write(error_trace)
    except Exception:
        pass

    # WSGI fallback to display the exact error instead of generic 500
    def application(environ, start_response):
        status = '500 Internal Server Error'
        body = (
            "<html><head><title>getNexiro Startup Error</title></head>"
            "<body style='font-family: monospace; padding: 24px; background: #080b10; color: #ff5555;'>"
            "<h2 style='color: #00f0ff;'>getNexiro â€” WSGI Startup Traceback</h2>"
            f"<pre style='background: #101520; color: #f8f8f2; padding: 18px; border-radius: 8px; border: 1px solid #222; overflow: auto;'>{error_trace}</pre>"
            "</body></html>"
        ).encode('utf-8')
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(body)))
        ]
        start_response(status, response_headers)
        return [body]

