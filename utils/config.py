from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WAKE_WORD = ["hey assistant", "wake up", " guess who's back"]  # Multiple wake words/phrases
SERIAL_PORT = 'COM8'  # Windows