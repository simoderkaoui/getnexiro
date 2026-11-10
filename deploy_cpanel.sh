#!/usr/bin/env bash
# ==============================================================================
# getNexiro — cPanel / Stellar Plus Deployment & Update Script
# Run this inside your cPanel Terminal or SSH:
#   cd ~/getnexiro && bash deploy_cpanel.sh
# ==============================================================================

set -e

echo "🚀 Starting getNexiro deployment on cPanel..."

# 1. Pull latest code from GitHub
if [ -d ".git" ]; then
    echo "⬇️  Pulling latest changes from GitHub (main)..."
    git pull origin main || echo "⚠️  Git pull skipped or has local changes."
fi

# 2. Install/update dependencies
echo "📦 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Apply database migrations
echo "🗄️  Applying database migrations..."
python manage.py migrate

# 4. Seed database with default data (if needed)
echo "🌱 Seeding multilingual database..."
python manage.py seed_data

# 5. Compile translations
echo "🌍 Compiling translation catalogs (.po -> .mo)..."
python compile_messages.py

# 6. Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# 7. Restart Phusion Passenger app
echo "🔄 Triggering Passenger application restart..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "✅ cPanel deployment and restart complete!"
