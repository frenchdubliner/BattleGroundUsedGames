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
GRANT ALL PRIVILEGES ON DATABASE your-db-name TO your-db-password;
\q
```

3. **Run migrations:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```