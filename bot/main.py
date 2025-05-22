# bot/main.py

from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
import os
import asyncio
import json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

bot = Client("control-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# User session & config store
CONFIG_FILE = "bot/config.json"
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f)


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply(
        "**Welcome to Forward Ai Bot!**\n\n"
        "Yeh bot aapko channel-to-channel auto forwarding system setup karne me madad karega.\n\n"
        "**Commands:**\n"
        "/login – Telegram account set karo (API ID, Hash, phone)\n"
        "/setsource – Source channel set karo\n"
        "/setdestination – Destination channel set karo\n"
        "/filter – Word filtering aur replace set karo\n"
        "/delfilter – Filter delete karo\n"
        "/filters – Saare filters dekho\n"
        "/startforward – Forwarding chalu karo\n"
        "/stopforward – Forwarding band karo\n"
        "/status – Current config dekho"
    )


@bot.on_message(filters.command("login"))
async def login_handler(_, message: Message):
    await message.reply(
        "Telegram login ke liye apne API ID, API HASH aur phone number bhejo is format me:\n\n"
        "`API_ID:API_HASH:PHONE`\n\n"
        "Example: `123456:abcde12345:+911234567890`",
        quote=True
    )


@bot.on_message(filters.text & filters.private)
async def save_login_details(_, message: Message):
    if ":" in message.text and message.text.count(":") == 2:
        api_id, api_hash, phone = message.text.split(":")
        config = load_config()
        config["api_id"] = api_id
        config["api_hash"] = api_hash
        config["phone"] = phone
        save_config(config)
        await message.reply("✅ Login details save ho gaye. Ab userbot run karo aur login kar lo.")
    else:
        pass  # not a login message


@bot.on_message(filters.command("setsource"))
async def set_source(_, message: Message):
    await message.reply("Source channel ka username ya ID bhejo:")


@bot.on_message(filters.command("setdestination"))
async def set_dest(_, message: Message):
    await message.reply("Destination channel ka username ya ID bhejo:")


@bot.on_message(filters.command("filter"))
async def filter_add(_, message: Message):
    await message.reply("Filter add karne ke liye is format me bhejo:\n`old_word:new_word`\nExample: `hello:hi`")


@bot.on_message(filters.command("delfilter"))
async def delfilter_list(_, message: Message):
    config = load_config()
    filters_list = config.get("filters", [])
    if not filters_list:
        await message.reply("❌ Koi filter set nahi hai.")
        return

    msg = "**Filters List:**\n"
    for idx, f in enumerate(filters_list):
        msg += f"{idx+1}. `{f['find']}` → `{f['replace']}`\n"
    msg += "\nDelete karne ke liye filter number bhejo."
    await message.reply(msg)


@bot.on_message(filters.command("filters"))
async def show_filters(_, message: Message):
    config = load_config()
    filters_list = config.get("filters", [])
    if not filters_list:
        await message.reply("❌ Abhi koi filters set nahi hai.")
        return

    msg = "**Current Filters:**\n"
    for f in filters_list:
        msg += f"- `{f['find']}` → `{f['replace']}`\n"
    await message.reply(msg)


@bot.on_message(filters.command("startforward"))
async def start_forward(_, message: Message):
    config = load_config()
    config["forwarding"] = True
    save_config(config)
    await message.reply("✅ Forwarding ON kar diya gaya.")


@bot.on_message(filters.command("stopforward"))
async def stop_forward(_, message: Message):
    config = load_config()
    config["forwarding"] = False
    save_config(config)
    await message.reply("⛔ Forwarding OFF kar diya gaya.")


@bot.on_message(filters.command("status"))
async def show_status(_, message: Message):
    config = load_config()
    status = "**Bot Status:**\n"
    status += f"Telegram Phone: `{config.get('phone', '❌ Not Set')}`\n"
    status += f"Source Channel: `{config.get('source', '❌ Not Set')}`\n"
    status += f"Destination Channel: `{config.get('destination', '❌ Not Set')}`\n"
    status += f"Forwarding: {'✅ ON' if config.get('forwarding') else '❌ OFF'}\n"
    await message.reply(status)


@bot.on_message(filters.text & filters.private)
async def handle_inputs(_, message: Message):
    text = message.text.strip()
    config = load_config()

    if "source" not in config:
        config["source"] = text
        save_config(config)
        await message.reply(f"✅ Source channel set ho gaya: `{text}`")
        return

    if "destination" not in config:
        config["destination"] = text
        save_config(config)
        await message.reply(f"✅ Destination channel set ho gaya: `{text}`")
        return

    if ":" in text:
        parts = text.split(":")
        if len(parts) == 2:
            find, replace = parts
            filters_list = config.get("filters", [])
            filters_list.append({"find": find, "replace": replace})
            config["filters"] = filters_list
            save_config(config)
            await message.reply(f"✅ Filter add ho gaya: `{find}` → `{replace}`")
            return

    # Filter delete by number
    if text.isdigit():
        idx = int(text) - 1
        filters_list = config.get("filters", [])
        if 0 <= idx < len(filters_list):
            removed = filters_list.pop(idx)
            config["filters"] = filters_list
            save_config(config)
            await message.reply(f"❌ Filter delete ho gaya: `{removed['find']}`")
        else:
            await message.reply("❌ Invalid number.")

bot.run()
