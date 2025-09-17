#!/data/data/com.termux/files/usr/bin/sh
# Launch bot on device boot (Termux:Boot)
cd ~/Advanced-AntiTheft-Bot
termux-wake-lock
nohup ./run_forever.sh &
