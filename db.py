# You don't need this directly, logic is inside bot.py/client.py
import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS filters (src TEXT, dst TEXT)")
conn.commit()
