"""WSGI entry point for gunicorn."""

import os
from pathlib import Path

# ensure project root is cwd
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

from app.main import create_app
from app.config import Settings

app = create_app(Settings())
