from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')  
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
    