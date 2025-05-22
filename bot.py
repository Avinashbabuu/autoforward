from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS filters (src TEXT, dst TEXT)")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Welcome to Channel Forward Bot!
Commands:
/addsource <channel_id>
/adddestination <channel_id>
/filter <bad> <good>
/listfilters
/delfilter <index>
/setsession
""")

async def addsource(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return await update.message.reply_text("Usage: /addsource <channel_id>")
    cur.execute("REPLACE INTO config (key, value) VALUES (?, ?)", ("source", context.args[0]))
    conn.commit()
    await update.message.reply_text("Source channel set.")

async def adddestination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return await update.message.reply_text("Usage: /adddestination <channel_id>")
    cur.execute("REPLACE INTO config (key, value) VALUES (?, ?)", ("destination", context.args[0]))
    conn.commit()
    await update.message.reply_text("Destination channel set.")

async def filter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /filter <bad> <good>")
    cur.execute("INSERT INTO filters (src, dst) VALUES (?, ?)", (context.args[0], context.args[1]))
    conn.commit()
    await update.message.reply_text("Filter added.")

async def listfilters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = cur.execute("SELECT rowid, src, dst FROM filters").fetchall()
    if not rows:
        return await update.message.reply_text("No filters.")
    msg = "\n".join([f"{r[0]}. {r[1]} -> {r[2]}" for r in rows])
    await update.message.reply_text(msg)

async def delfilter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1 or not context.args[0].isdigit():
        return await update.message.reply_text("Usage: /delfilter <index>")
    cur.execute("DELETE FROM filters WHERE rowid = ?", (context.args[0],))
    conn.commit()
    await update.message.reply_text("Filter deleted.")

async def setsession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please run `python client.py` to set up your Telegram user session.")

app = ApplicationBuilder().token("8016050256:AAGU-eLX0gZaQYYDJ4bNwjYDIVsO2Glzp3s").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addsource", addsource))
app.add_handler(CommandHandler("adddestination", adddestination))
app.add_handler(CommandHandler("filter", filter_cmd))
app.add_handler(CommandHandler("listfilters", listfilters))
app.add_handler(CommandHandler("delfilter", delfilter))
app.add_handler(CommandHandler("setsession", setsession))
app.run_polling()
