# config.py
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
LOG_FILE_PATH = BASE_DIR / 'desktop.log'

# API Configuration
# Change this to your actual server URL when deploying
API_BASE_URL = "http://127.0.0.1:8000/api/"
AUTH_URL = "http://127.0.0.1:8000/facilitator/login/"
LOGOUT_URL = "http://127.0.0.1:8000/facilitator/logout/"
JWT_AUTH_URLS = [
    "http://127.0.0.1:8000/api/token/",
    "http://127.0.0.1:8000/api/jwt/create/",
]
TOKEN_AUTH_URLS = [
    "http://127.0.0.1:8000/api-token-auth/",
    "http://127.0.0.1:8000/api/token-auth/",
]

# App Configuration
APP_NAME = "School Voting System - Staff Desktop"
APP_VERSION = "1.0.0"
APP_WIDTH = 1280
APP_HEIGHT = 720

# Database (for local cache if needed)
DATABASE_PATH = BASE_DIR / 'local_cache.db'

# Session timeout (in minutes)
SESSION_TIMEOUT = 30

# File upload settings
MAX_CSV_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CSV_COLUMNS = ['student_id', 'first_name', 'last_name', 'course', 'year', 'email']
ALLOWED_YEAR_LEVELS = ['1', '2', '3', '4', '5', '6']

# Theme colors
COLORS = {
    'primary': '#4CAF50',
    'secondary': '#2196F3',
    'danger': '#f44336',
    'warning': '#FF9800',
    'dark': '#333333',
    'light': '#f5f5f5',
    'white': '#ffffff',
    'success': '#4CAF50'
}
