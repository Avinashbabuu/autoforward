#!/bin/bash

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Starting bot and client ==="
# Run bot in background
nohup python3 bot.py > bot.log 2>&1 &
# Run client in background
nohup python3 client.py > client.log 2>&1 &

echo "Bot and client are now running in background."
