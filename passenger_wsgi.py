import os
import sys
import glob

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Auto-detect cPanel virtualenv Python interpreter and site-packages
home = os.path.expanduser("~")
venv_pythons = (
    glob.glob(os.path.join(home, "virtualenv", "getnexiro", "*", "bin", "python")) +
    glob.glob(os.path.join(home, "virtualenv", "*", "*", "bin", "python"))
)

if venv_pythons:
    interp = venv_pythons[0]
    if sys.executable != interp and os.path.exists(interp):
        try:
            os.execl(interp, interp, *sys.argv)
        except Exception:
            pass

# Add virtualenv site-packages to sys.path
venv_site_packages = (
    glob.glob(os.path.join(home, "virtualenv", "getnexiro", "*", "lib", "python*", "site-packages")) +
    glob.glob(os.path.join(home, "virtualenv", "*", "*", "lib", "python*", "site-packages"))
)
for sp in venv_site_packages:
    if sp not in sys.path:
        sys.path.insert(0, sp)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getnexiro.settings')

# Wrap WSGI loading to capture startup errors
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception:
    import traceback
    error_trace = traceback.format_exc()
    
    # Save traceback to file for diagnosis
    try:
        with open(os.path.join(BASE_DIR, "passenger_error.log"), "w", encoding="utf-8") as f:
            f.write(error_trace)
    except Exception:
        pass

    # WSGI fallback to display the exact error instead of generic 500
    def application(environ, start_response):
        status = '500 Internal Server Error'
        body = (
            "<html><head><title>Startup Error</title></head>"
            "<body style='font-family: monospace; padding: 20px; background: #111; color: #f55;'>"
            "<h2>getNexiro Startup Error</h2>"
            f"<pre style='background: #222; padding: 15px; border-radius: 6px; overflow: auto;'>{error_trace}</pre>"
            "</body></html>"
        ).encode('utf-8')
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(body)))
        ]
        start_response(status, response_headers)
        return [body]
