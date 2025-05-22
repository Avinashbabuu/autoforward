# userbot/forwarder.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from telethon import TelegramClient, events
from userbot.session_manager import login_userbot
from dotenv import load_dotenv
import json

# Load .env file
load_dotenv()

# Path to configuration file
CONFIG_FILE = "bot/config.json"

# Load configuration
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Forward message and apply filters
async def forward_message(client, message):
    config = load_config()
    source_channel = config.get("source")
    destination_channel = config.get("destination")

    if not source_channel or not destination_channel:
        print("❌ Source ya Destination channel set nahi hai.")
        return

    # Apply filters if present
    filters = config.get("filters", [])
    for filter in filters:
        if filter["find"] in message.text:
            message.text = message.text.replace(filter["find"], filter["replace"])

    # Forward message
    await client.send_message(destination_channel, message.text)
    print(f"✅ Message forwarded from {source_channel} to {destination_channel}")


async def main():
    client = await login_userbot()
    if client:
        @client.on(events.NewMessage(chats=None))  # Listen to all new messages
        async def my_event_handler(event):
            # Only forward if message is from the source channel
            config = load_config()
            source_channel = config.get("source")
            if event.chat_id == source_channel:
                await forward_message(client, event.message)

        # Start client event loop
        print("🔄 Forwarding started...")
        await client.run_until_disconnected()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
