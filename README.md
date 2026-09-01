# getNexiro — Premium B2B Software Development Agency

<p align="center">
  <strong>get</strong><span style="color: #c9a84c;">Nexiro</span>
</p>

> A luxury B2B software development agency website, based in Tangier, Morocco.  
> Built with Django, featuring trilingual support (English, French, Arabic with RTL).

---

## 🏗️ Tech Stack

- **Backend:** Django 5.1+
- **Frontend:** Custom CSS (dark luxury theme) + vanilla JavaScript
- **i18n:** Django's built-in internationalization framework
- **Languages:** English (en), French (fr), Arabic (ar) with RTL support
- **Database:** SQLite (development)

---

## 📂 Project Structure

```
getnexiro/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── getnexiro/                 # Project configuration
│   ├── __init__.py
│   ├── settings.py            # Settings with i18n config
│   ├── urls.py                # Root URL config with i18n_patterns
│   └── wsgi.py
├── core/                      # Main application
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py                # App URL patterns
│   ├── views.py               # Page views
│   ├── forms.py               # Contact form
│   └── models.py              # Models (extensible)
├── templates/
│   ├── base.html              # Base template (navbar + footer)
│   └── core/
│       ├── home.html           # Landing page
│       ├── about.html          # About the agency
│       ├── services.html       # Services offered
│       ├── projects.html       # Portfolio / case studies
│       ├── store.html          # Store (coming soon)
│       └── contact.html        # Contact form + info
├── static/
│   ├── css/
│   │   ├── main.css           # Main luxury dark theme
│   │   └── rtl.css            # RTL overrides for Arabic
│   └── js/
│       └── main.js            # Navigation, filters, animations
└── locale/
    ├── en/LC_MESSAGES/django.po  # English (source)
    ├── fr/LC_MESSAGES/django.po  # French translations
    └── ar/LC_MESSAGES/django.po  # Arabic translations
```

---

## 🚀 Quick Start

### 1. Clone & Enter the Project

```bash
cd getnexiro
```

### 2. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Compile Translation Files

Compile the `.po` files into `.mo` binary files used by Django at runtime:

```bash
python manage.py compilemessages
```

> **Note:** On Windows, you may need to install [GNU gettext](https://mlocati.github.io/articles/gettext-iconv-windows.html) for `compilemessages` to work. Alternatively, you can use the pre-compiled `.mo` files if they are already present.

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to view the site.

---

## 🌐 Language Switching

The site supports three languages with URL prefixes:

| Language | URL Prefix | Direction |
|----------|-----------|-----------|
| English  | `/en/`    | LTR       |
| French   | `/fr/`    | LTR       |
| Arabic   | `/ar/`    | RTL       |

- Use the **language switcher** in the navbar or footer to switch languages.
- Arabic pages automatically render with `dir="rtl"` and load the RTL stylesheet.

---

## 📄 Pages

| Page       | URL Path    | Description |
|------------|-------------|-------------|
| Home       | `/`         | Hero, value proposition, featured services & projects, CTA |
| About      | `/about/`   | Agency story, mission, why Tangier, team, values |
| Services   | `/services/`| Full service list with process section |
| Projects   | `/projects/`| Filterable portfolio grid with case studies |
| Store      | `/store/`   | Coming soon placeholder |
| Contact    | `/contact/` | Contact form + agency info + map |

---

## 🔧 Development Commands

### Update Translation Strings

When you add new translatable strings, extract them:

```bash
python manage.py makemessages -l fr
python manage.py makemessages -l ar
```

Then translate the new entries in the `.po` files and compile:

```bash
python manage.py compilemessages
```

### Collect Static Files (Production)

```bash
python manage.py collectstatic
```

---

## 🎨 Design System

- **Color Palette:** Dark navy/black (#0a0a0f) with gold (#c9a84c) accents
- **Typography:** Playfair Display (headings) + Inter (body)
- **Responsive:** Mobile-first, breakpoints at 480px, 768px, 1024px
- **Animations:** Scroll-reveal, subtle hover transitions

---

## 📝 Placeholder Images

All images use [Picsum Photos](https://picsum.photos) placeholders. Replace the URLs in `views.py` and templates with your actual images for production.

---

## 📜 License

© 2025 getNexiro. All rights reserved.

---

## 🔗 Social Media

- Instagram: [@getnexiro](https://www.instagram.com/getnexiro)
