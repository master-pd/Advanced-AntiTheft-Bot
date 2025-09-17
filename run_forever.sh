#!/bin/bash
# run_forever.sh - keep the bot running; restart on crash
REPO_DIR=~/Advanced-AntiTheft-Bot
LOG=$REPO_DIR/runner.log
while true; do
  echo "$(date) - starting bot" >> "$LOG"
  python "$REPO_DIR/anti_theft_advanced.py" >> "$LOG" 2>&1
  echo "$(date) - bot stopped, restarting in 5s" >> "$LOG"
  sleep 5
done
