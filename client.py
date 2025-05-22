from telethon.sync import TelegramClient, events
import sqlite3
import os

conn = sqlite3.connect("data.db")
cur = conn.cursor()
api_id = int(input("Enter your api_id: "))
api_hash = input("Enter your api_hash: ")
phone = input("Enter your phone number: ")

with TelegramClient("user_session", api_id, api_hash) as client:
    client.start(phone=phone)

    source = cur.execute("SELECT value FROM config WHERE key='source'").fetchone()
    destination = cur.execute("SELECT value FROM config WHERE key='destination'").fetchone()
    filters = cur.execute("SELECT src, dst FROM filters").fetchall()

    if not source or not destination:
        print("Please set source and destination channel using bot first.")
        exit(1)

    source_channel = source[0]
    destination_channel = destination[0]

    @client.on(events.NewMessage(chats=int(source_channel)))
    async def handler(event):
        text = event.raw_text
        for src, dst in filters:
            text = text.replace(src, dst)
        await client.send_message(entity=int(destination_channel), message=text)

    print("Listening for new messages...")
    client.run_until_disconnected()
