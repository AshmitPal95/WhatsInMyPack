from google import genai
from dotenv import load_dotenv
import os

load_dotenv("api_key.env")

def gemini_client():
    return genai.Client(api_key=os.getenv("api_key"))