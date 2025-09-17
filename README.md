# Advanced-AntiTheft-Bot

Powerful Termux-compatible Telegram Anti-Theft bot. Use only on your own device.

## Features
- Password protected admin commands
- Location (GPS), Photo, Alarm, Lock attempt
- Heartbeat, Geofence, SIM-change detection
- Auto-update from GitHub (optional)
- Watchdog wrapper & Termux:Boot support

## Install (Termux)
1. Update & install packages:
   ```bash
   pkg update -y && pkg upgrade -y
   pkg install python git termux-api -y

   
