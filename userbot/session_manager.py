# userbot/session_manager.py

import os
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
SESSION_FILE = "userbot/forward_user.session"

async def login_userbot():
    if not all([API_ID, API_HASH, PHONE]):
        print("❌ API ID, API HASH ya PHONE missing hai .env file se.")
        return None

    client = TelegramClient(SESSION_FILE, int(API_ID), API_HASH)

    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(PHONE)
            code = input("Telegram se aaya code daalo: ")
            await client.sign_in(PHONE, code)
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return None

    print("✅ Userbot login successful.")
    return client
