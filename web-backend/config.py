# config.py
from dotenv import load_dotenv
import os

load_dotenv()

MAILERSEND_API_KEY = os.environ.get('MAILERSEND_API_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
