# Production Deployment Guide — getnexiro.com

This guide provides complete, production-tested instructions to deploy **getNexiro** to **https://getnexiro.com**.

---

## 📋 Architectural Overview

- **Framework:** Django 5.x (Python 3.11, 3.12, 3.14 compatible)
- **Production Server:** Gunicorn + Nginx (VPS) OR PythonAnywhere WSGI
- **Database:** SQLite (default, self-contained, zero-downtime backups) or PostgreSQL
- **Languages:** English (`/en/`), French (`/fr/`), Arabic (`/ar/` with full native RTL)
- **Theme:** Exclusively dark luxury (`#080b10`, cyan & electric indigo glow)
- **Static Assets:** Whitenoise / Nginx static directory (`staticfiles/`)
- **SEO & PWA:** Multi-resolution favicons, Apple touch icon, `site.webmanifest`, localized XML sitemaps, robots.txt

---

## 🚀 Option 1: PythonAnywhere Deployment (Recommended & Fastest)

PythonAnywhere is ideal for getNexiro because the application is fully self-contained with no Celery/Redis dependencies.

### Step 1: Open a Bash Console on PythonAnywhere
Log in to your PythonAnywhere account and start a **Bash console**.

### Step 2: Clone the Repository
```bash
git clone https://github.com/athen676/nifty-oppenheimer.git getNexiro
cd getNexiro
```

### Step 3: Create & Activate Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.11 getnexiro-env
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Production Environment Variables (`.env`)
Create your production `.env` file:
```bash
cp .env.example .env
nano .env
```
Fill in the following key variables:
```ini
SECRET_KEY=generate-a-strong-random-key-here-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=getnexiro.com,www.getnexiro.com,yourusername.pythonanywhere.com
SITE_URL=https://getnexiro.com

# SMTP Email Configuration (Gmail App Password)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=getnexiro@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-gmail-app-password
DEFAULT_FROM_EMAIL=getNexiro <getnexiro@gmail.com>
SERVER_EMAIL=getNexiro <getnexiro@gmail.com>
```
*(To get a Gmail App Password: Go to Google Account > Security > 2-Step Verification > App Passwords > Generate for "getNexiro")*

### Step 5: Run Migrations, Seed Database & Collect Static Files
```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```
Create your superuser for `/admin/`:
```bash
python manage.py createsuperuser
```

### Step 6: Configure the PythonAnywhere Web Tab
1. Navigate to the **Web** tab in the PythonAnywhere dashboard.
2. Click **Add a new web app** (choose **Manual configuration**, then **Python 3.11**).
   - If using custom domain: enter `getnexiro.com` or `www.getnexiro.com`.
3. Set **Virtualenv**:
   `/home/<your-username>/.virtualenvs/getnexiro-env`
4. Set **Source code**:
   `/home/<your-username>/getNexiro`
5. Set **Working directory**:
   `/home/<your-username>/getNexiro`

### Step 7: Configure Static Files Mappings (Web Tab)
Add two entries in the **Static files** section:

| URL | Path |
| :--- | :--- |
| `/static/` | `/home/<your-username>/getNexiro/staticfiles` |
| `/media/` | `/home/<your-username>/getNexiro/media` |

### Step 8: Configure the WSGI File
Click on the **WSGI configuration file** link (e.g., `/var/www/<domain>_wsgi.py`), delete everything, and paste:

```python
import os
import sys

# Path to project
path = '/home/<your-username>/getNexiro'
if path not in sys.path:
    sys.path.insert(0, path)

# Virtual environment python packages
venv_path = '/home/<your-username>/.virtualenvs/getnexiro-env/lib/python3.11/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'getnexiro.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `<your-username>` with your actual PythonAnywhere username)*.

### Step 9: Enable HTTPS & Reload
- In the Web tab, under **Security**, enable **Force HTTPS**.
- Click the green **Reload <domain>** button at the top.
- Visit `https://getnexiro.com`!

---

## 🌐 DNS Setup for getnexiro.com

Point your domain name registrar (Namecheap, GoDaddy, Cloudflare, etc.) to your hosting provider:

### For PythonAnywhere Custom Domain:
- **CNAME Record**: Host `www` -> Value `webapp-<number>.pythonanywhere.com`
- **A Record / ALIAS / ANAME**: Host `@` -> Point to PythonAnywhere IP or forward `@` to `www.getnexiro.com`.

---

## 🖥️ Option 2: Ubuntu VPS Deployment (Gunicorn + Nginx + Let's Encrypt)

If deploying to a VPS (DigitalOcean, Hetzner, AWS EC2, Linode):

### 1. System Packages
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx git certbot python3-certbot-nginx
```

### 2. Clone & Setup
```bash
sudo git clone https://github.com/athen676/nifty-oppenheimer.git /var/www/getnexiro
cd /var/www/getnexiro
sudo python3 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install -r requirements.txt
sudo cp .env.example .env
sudo nano .env
sudo ./venv/bin/python manage.py migrate
sudo ./venv/bin/python manage.py seed_data
sudo ./venv/bin/python manage.py collectstatic --noinput
sudo chown -R www-data:www-data /var/www/getnexiro
```

### 3. Systemd Gunicorn Service (`/etc/systemd/system/getnexiro.service`)
```ini
[Unit]
Description=getNexiro Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/getnexiro
ExecStart=/var/www/getnexiro/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/run/getnexiro.sock \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          getnexiro.wsgi:application

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo mkdir -p /var/log/gunicorn
sudo systemctl daemon-reload
sudo systemctl start getnexiro
sudo systemctl enable getnexiro
```

### 4. Nginx Configuration (`/etc/nginx/sites-available/getnexiro`)
```nginx
server {
    server_name getnexiro.com www.getnexiro.com;

    client_max_body_size 25M;

    # Static files with 30-day cache
    location /static/ {
        alias /var/www/getnexiro/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Media files with 7-day cache
    location /media/ {
        alias /var/www/getnexiro/media/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    # Favicon and Manifest directly served
    location = /favicon.ico {
        alias /var/www/getnexiro/staticfiles/images/favicon.ico;
    }
    location = /site.webmanifest {
        alias /var/www/getnexiro/staticfiles/site.webmanifest;
    }

    # Gunicorn reverse proxy
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/getnexiro.sock;
    }
}
```

Enable site & get SSL certificate:
```bash
sudo ln -s /etc/nginx/sites-available/getnexiro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d getnexiro.com -d www.getnexiro.com
```

---

## ✅ Post-Deployment Verification Checklist

Once deployed, verify each of these endpoints:

1. **Homepage:** `https://getnexiro.com/en/` — Hero video, dark luxury design, floating WhatsApp button (`wa.me/212787862187`).
2. **Language Switching:**
   - French: `https://getnexiro.com/fr/`
   - Arabic: `https://getnexiro.com/ar/` (Verify RTL layout, Cairo typography, mirrored buttons).
3. **PWA & Favicon:**
   - `https://getnexiro.com/favicon.ico` returns 200 / valid icon.
   - `https://getnexiro.com/site.webmanifest` returns 200 with JSON manifest.
4. **Local SEO:**
   - `https://getnexiro.com/en/services/web-development/web-development-tangier/`
   - `https://getnexiro.com/ar/خدمات/web-development/web-development-tangier/`
5. **Interactive Wizards & Forms:**
   - Quote Wizard: `https://getnexiro.com/en/quote/`
   - Discovery Booking: `https://getnexiro.com/en/booking/`
   - Contact Form: `https://getnexiro.com/en/contact/`
   - Verify confirmation emails arrive in the submitter's inbox and admin notification arrives at `getnexiro@gmail.com`.
6. **Search Engine Discovery:**
   - Robots: `https://getnexiro.com/robots.txt`
   - Multilingual Sitemap: `https://getnexiro.com/sitemap.xml`
7. **Admin Dashboard:** `https://getnexiro.com/admin/`
