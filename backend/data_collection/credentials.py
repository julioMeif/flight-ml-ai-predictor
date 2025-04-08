# credentials.py
from dotenv import load_dotenv
import os

load_dotenv()

AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")