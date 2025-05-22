#!/bin/bash

echo "Starting Telegram Forwarding System..."

# Activate virtual environment if used (uncomment if needed)
# source venv/bin/activate

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run the bot and userbot scripts in background
python3 bot/main.py & 
python3 userbot/forwarder.py &

echo "Bot and Userbot started successfully."
