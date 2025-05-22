# Telegram Channel-to-Channel Forwarder Bot

This bot forwards messages from a source Telegram channel to a destination channel using a user account (not bot), with support for message filtering and replacement.

## Features
- Forward messages using Telegram user account
- Add filters to replace words in forwarded messages
- Telegram bot control panel to manage channels, filters, and session setup

## Commands
- /start - Show welcome message and all commands
- /addsource - Set source channel ID
- /adddestination - Set destination channel ID
- /filter - Add a filter (e.g., `bad good` to replace 'bad' with 'good')
- /listfilters - Show current filters
- /delfilter - Delete filter by index
- /setsession - Guide to set up Telegram user session

## Setup Instructions

### 1. Clone the repo and install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run both scripts in separate terminals
```bash
python bot.py      # Starts the control panel bot
python client.py   # Starts the forwarder using your Telegram account
```

### 3. Create a session
- Bot will ask for your `api_id`, `api_hash`, and phone number to create session.
