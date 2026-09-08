#!/usr/bin/env bash
# ==============================================================================
# getNexiro — PythonAnywhere Deployment Script
# Run this inside your PythonAnywhere Bash console:
#   cd ~/getnexiro && bash deploy_pa.sh
# ==============================================================================

set -e

echo "🚀 Starting getNexiro deployment on PythonAnywhere..."

# 1. Activate virtual environment if available
if [ -d "$HOME/.virtualenvs/myenv" ]; then
    echo "📦 Activating virtualenv: ~/.virtualenvs/myenv"
    source "$HOME/.virtualenvs/myenv/bin/activate"
elif [ -d "venv" ]; then
    echo "📦 Activating virtualenv: ./venv"
    source venv/bin/activate
fi

# 2. Pull latest code from GitHub
echo "⬇️  Pulling latest changes from GitHub (main)..."
git pull origin main

# 3. Install/update dependencies
echo "📦 Installing requirements..."
pip install -r requirements.txt

# 4. Apply database migrations
echo "🗄️  Applying database migrations..."
python manage.py migrate

# 5. Seed database with multilingual data (if needed)
echo "🌱 Seeding multilingual database..."
python manage.py seed_data

# 6. Compile translations
echo "🌍 Compiling translation catalogs (.po -> .mo)..."
python compile_messages.py

# 7. Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Deployment complete!"
echo "👉 Now click the green 'Reload' button on your PythonAnywhere Web tab."
