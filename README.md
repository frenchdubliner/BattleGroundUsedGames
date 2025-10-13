# Install project on ubuntu server

## Prerequisites

1. **Update your system:**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Python and pip:**
```bash
sudo apt install python3 python3-pip python3-venv -y
```

3. **Install Nginx:**
```bash
sudo apt install nginx -y
```

4. **Install PostgreSQL (database recommended for production):**
```bash
sudo apt install postgresql postgresql-contrib -y
```

5. **Install tex (used to generate pdf):**
```bash
sudo apt install texlive-full texlive-latex-recommended -y
```

6. **Install pdftk (used to generate pdf):**
```bash
sudo apt install pdftk -y
```

7. **Install git:**
```bash
sudo apt install git -y
```

8. **Install libpq-dev (used to generate fake games to test the load):**
```bash
sudo apt-get install libpq-dev -y
```

## Step 1: Set up the project

1. **Clone the project in the folder you want:**
```bash
git clone https://github.com/frenchdubliner/BattleGroundUsedGames.git
```

2. **Navigate to your project directory (your_directory is the location of your directory):**
```bash
cd your_directory
```

3. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install gunicorn
```

## Step 2: Environment Configuration

1. **Create a `.env` file in your project root:**
```bash
nano .env
```

2. **Add the following content:**
```env
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
DEBUG=False
LIST_HOST_PRODUCTION=your-domain.com,your-server-ip

DB_NAME=your-db-name
DB_USER=your-db-password
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=your-db-port
LIST_USERNAME_BLACKLIST=username_1,username_2,usernam_3
```

3. **Generate a new secret key then add this to env:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 3: 1 & 2 only if database is local database

1. **Create a PostgreSQL database:**
```bash
sudo -u postgres psql
```

2. **In PostgreSQL shell:**
```sql
CREATE DATABASE your-db-name;
CREATE USER your-db-user WITH PASSWORD 'your-db-password';
GRANT ALL PRIVILEGES ON DATABASE your-db-name TO your-db-user;
\q
```

3. **Run migrations:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Step 4: Create Gunicorn Service

1. **Create a systemd service file:**
```bash
sudo nano /etc/systemd/system/battleground.service
```

2. **Add the following content (replace your_user and your_path with the correct values):**
```ini
[Unit]
Description=BattleGround Django App
After=network.target

[Service]
Type=notify
User=your_user
Group=www-data
WorkingDirectory=/home/your_user/BattleGroundUsedGames
Environment="PATH=/home/your_user/BattleGroundUsedGames/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="DJANGO_SETTINGS_MODULE=a_core.settings"
ExecStart=/home/your_user/BattleGroundUsedGames/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 a_core.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

3. **Start and enable the service:**
```bash
sudo systemctl start battleground
sudo systemctl enable battleground
sudo systemctl status battleground
```

## Step 5: Configure Nginx

1. **Create Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/battleground
```

2. **Add the following configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com your-server-ip;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /exports/ {
        alias /var/www/your_website/exports/;
        expires 1h;
        add_header Cache-Control "public, no-cache";
    }
    
    location /static/ {
        alias /home/your_user_folder/BattleGroundUsedGames/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/your_user_folder/BattleGroundUsedGames/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

3. **Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/battleground /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

4. **Enable SSL:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain_or_server_ip
sudo nginx -t
sudo systemctl restart nginx
```


## Maintenance: 

1. **Saving database:**
```bash
pg_dump -U your_db_user -h localhost -Fc your_db_name > db.dump
```

2. **Restoring database:**
```bash
pg_restore -h 127.0.0.1 -U your_db_user -d your_db_name db.dump
```

3. **Cleaning database before restoring if there are errors:**
```bash
sudo -u postgres dropdb your_db_name
sudo -u postgres createdb your_db_name -O your_db_user

```


4. **Restart Services:**
```bash
sudo systemctl restart nginx
sudo systemctl restart battleground

```


5. **Check Logs:**
```bash
# 1. Check Django application logs (adjust service name as needed)
sudo journalctl -u gunicorn -f
sudo journalctl -u uwsgi -f
sudo journalctl -u your-django-app -f

# 2. Check system logs
sudo journalctl -f | grep -i latex
sudo journalctl -f | grep -i pdflatex

# 3. Check if there are any log files in your Django project directory
ls -la /var/www/your_website/logs/
tail -f /var/www/your_website/logs/*.log

# 4. Check the exports directory for any temporary files
ls -la /var/www/your_website/exports/

# Check Django application logs (if using systemd)
sudo journalctl -u your-django-service-name -f

# Or check if you have a specific log file for your Django app
tail -f /var/log/django.log
tail -f /var/log/your-app.log

# Check system logs for any pdflatex errors
sudo journalctl -f | grep 

# 5. Resolve access problems
sudo adduser your_user www-data
sudo chown -R your_user:www-data /home/your_user/BattleGroundUsedGames/staticfiles
sudo chmod -R 755 /home/your_user/BattleGroundUsedGames/staticfiles

```

6. **Seed  Games for Testing:**
```bash
python manage.py seed_games --number 20
```