from chat_interface import run_chat
from bq_utils import get_bq_client

KEY_PATH = r"C:\Users\Asus VivoBook\Desktop\project\key_YT.json"
PROJECT_ID = "our-brand-487710-b8"

client = get_bq_client(KEY_PATH, PROJECT_ID)

run_chat(client)