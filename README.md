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


