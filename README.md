সব setup & run commands (Termux)

Config & messages template

Logs setup

Background & auto-run

File structure

Author, License, Tips সব একসাথে


এই ফাইল একবারে copy-paste করে GitHub repo তে save করা যাবে, আর কিছু আলাদা করতে হবে না।


---

# Advanced-AntiTheft-Bot

**Advanced-AntiTheft-Bot** হল একটি Termux & Python-ভিত্তিক Telegram Bot যা মোবাইল ডিভাইসের জন্য anti-theft ও নিরাপত্তা ফিচার প্রদান করে।  
এই README.md-তে সবকিছু একসাথে দেওয়া হলো: setup, run, config, messages, logs, file structure, author, license, tips।

---

## 📦 Features

- Telegram Bot মাধ্যমে real-time নোটিফিকেশন  
- Custom messages পাঠানো এবং লগ রাখা (Success / Fail)  
- Configurable Bot Token, Admin Chat ID, এবং Password  
- Termux compatible: Python 3 & Git support  
- Background mode & auto-run after reboot  
- Logs folder: Success_log.txt & Fail_log.txt  
- Easy setup & single-command installation  

---

## ⚙️ Full Setup & Run (Termux) — সব ধাপ একসাথে

নিচের ধাপগুলো **একবারে copy-paste করো** Termux-এ:

```bash
# ১. Update Termux & install packages
pkg update -y
pkg upgrade -y
pkg install python -y
pkg install git -y
pkg install nano -y
```

# ২. Clone GitHub repo
```
cd ~
rm -rf Advanced-AntiTheft-Bot
git clone https://github.com/master-pd/Advanced-AntiTheft-Bot.git
cd Advanced-AntiTheft-Bot
```

# ৩. Install Python dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
# ৪. Make scripts executable
```
chmod +x main.py run_forever.sh termux-boot.sh
```
# ৫. Setup config.json with template
````
cat <<EOL > config.json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "admin_chat_id": "YOUR_CHAT_ID",
  "password": "YOUR_PASSWORD"
}
EOL
````
# ৬. Setup messages.txt with all messages
```
cat <<EOL > messages.txt
হাই! কেমন আছো?
আজকের দিনটা কেমন যাচ্ছে?
মজা করছে তো?
কোথায় আছো আজ?
সব ঠিক আছে তো?
যাই হোক মূল কথায় আসি।
নতুন মেসেজ ১
নতুন মেসেজ ২
নতুন মেসেজ ৩
নতুন মেসেজ ৪
নতুন মেসেজ ৫
নতুন মেসেজ ৬
নতুন মেসেজ ৭
নতুন মেসেজ ৮
নতুন মেসেজ ৯
নতুন মেসেজ ১০
EOL
````

# ৭. Create logs folder & files
```
mkdir -p logs
touch logs/Success_log.txt logs/Fail_log.txt
```
# ৮. Run bot
```
python main.py
```
# ৯. Run in background (optional)
```
nohup python main.py &
```
# 🔟 Auto-run after reboot (optional)
```
cp termux-boot.sh ~/.termux/boot/
```

---

🗂️ File Structure
```
Advanced-AntiTheft-Bot/
│
├── main.py
├── messages.txt
├── config.json
├── run_forever.sh
├── termux-boot.sh
├── requirements.txt
├── logs/
│   ├── Success_log.txt
│   └── Fail_log.txt
├── assets/
├── web/
├── README.md
├── LICENSE
└── SECURITY.md


---
```

# ⚠️ Notes

প্রথমবার রান করার আগে **config.json এবং messages.txt চেক করা আবশ্যক।

Bot Token ও Admin Chat ID সঠিকভাবে বসাতে হবে।

Termux 100% compatible, Python 3.12+ ব্যবহার করুন।


Logs folder & files auto-create হয়, যদি না থাকে।



---


# 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.


---

# ⚡ Author

Md Rana Sheikh – Telegram Bot & Android Security Enthusiast
Email: mdranasheikhe2005@gmail.com


---

# 🔹 Tips

সর্বদা pip install --upgrade pip ব্যবহার করো।

নতুন messages যুক্ত করতে messages.txt এ লাইন যোগ করো।

Auto-run & background mode নিশ্চিত করতে run_forever.sh ও termux-boot.sh executable করতে হবে।


---






## One Click copy past 

Complete Command ✅⤵️

# ==== BEGIN FULL ONE-CLICK ADVANCED-ANTITHEFT-BOT SETUP ====

# 1️⃣ Termux update & packages
pkg update -y && pkg upgrade -y
pkg install -y python clang make openssl libffi git curl jq build-essential libcrypt-dev nano

# 2️⃣ Python pip upgrade
python -m pip install --upgrade pip setuptools wheel

# 3️⃣ Fix problematic packages
pip install --no-cache-dir cffi cryptography

# 4️⃣ Clone Bot repo
cd ~
rm -rf Advanced-AntiTheft-Bot
git clone https://github.com/master-pd/Advanced-AntiTheft-Bot.git || { echo "git clone failed"; exit 1; }
cd Advanced-AntiTheft-Bot || { echo "cd failed"; exit 1; }

# 5️⃣ Install requirements
pip install --no-cache-dir -r requirements.txt || echo "Some packages failed, check logs"

# 6️⃣ Create config.json
cat <<'JSON' > config.json
{
  "bot_token": "8124079918:AAEsXKzx8Lxk2Qqo1gzOC2J5U7G3GuvH44g",
  "admin_chat_id": "6454347745",
  "password": "r4nA#T0p!9kLm2$Z"
}
JSON

# 7️⃣ Create messages.txt
cat <<'MSG' > messages.txt
🔒 Device Security Alert!
📍 Location request received.
⚡ Power disconnected!
🔋 Power connected!
📶 SIM card changed!
🚨 Unauthorized access detected!
✅ Task completed successfully.
❌ Task failed, please check logs.
MSG

# 8️⃣ Logs & permissions
mkdir -p logs
touch logs/Success_log.txt logs/Fail_log.txt
chmod +x *.sh || true
chmod +x main.py || true

# 9️⃣ run_forever.sh (auto-restart)
cat <<'SH' > run_forever.sh
#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")"
while true; do
  python main.py
  echo "$(date "+%Y-%m-%d %H:%M:%S") - main.py exited with code $?. Restarting in 3s..." >> logs/Fail_log.txt
  sleep 3
done
SH
chmod +x run_forever.sh

# 🔟 Auto test script (all events)
cat <<'EOL' > test_all_events.py
import time
from main import send_message

events = [
    "🔒 Device Security Alert!",
    "📍 Location request received.",
    "⚡ Power disconnected!",
    "🔋 Power connected!",
    "📶 SIM card changed!",
    "🚨 Unauthorized access detected!",
    "✅ Task completed successfully.",
    "❌ Task fail
