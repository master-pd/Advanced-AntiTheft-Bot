#!/usr/bin/env python3
# anti_theft_advanced.py
# Advanced Anti-Theft bot (synchronous; python-telegram-bot v13)

import time
import logging
import requests
import threading
import base64
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from cryptography.fernet import Fernet

# --------- Load config ---------
CFG_FILE = os.path.expanduser("~/Advanced-AntiTheft-Bot/config.json")
if not os.path.exists(CFG_FILE):
    # try local
    CFG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

with open(CFG_FILE, 'r') as f:
    cfg = json.load(f)

BOT_TOKEN = cfg.get('bot_token')
PASSWORD = cfg.get('password')
ADMIN_CHAT_ID = cfg.get('admin_chat_id')
HEARTBEAT_MIN = int(cfg.get('heartbeat_min', 30))
GEOFENCE_RADIUS_M = int(cfg.get('geofence_radius_m', 200))
AUTO_UPDATE = bool(cfg.get('auto_update_github', False))
GITHUB_REPO = cfg.get('github_repo')
CLOUD_BACKUP = bool(cfg.get('cloud_backup', False))

# paths
STORE_FILE = os.path.expanduser('~/Advanced-AntiTheft-Bot/store.json')
LOGFILE = os.path.expanduser('~/Advanced-AntiTheft-Bot/anti_theft.log')
ASSETS_DIR = os.path.expanduser('~/Advanced-AntiTheft-Bot/assets')
ALARM_FILE = os.path.join(ASSETS_DIR, 'alarm.mp3')

# ---------- Logger ----------
logger = logging.getLogger('anti_theft')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGFILE)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

# ---------- Helpers ----------
def run_cmd(cmd, timeout=10):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        return out.decode('utf-8', errors='ignore').strip()
    except subprocess.CalledProcessError as e:
        return f"ERR: {e.output.decode(errors='ignore')}"
    except Exception as e:
        return f"ERR: {e}"

def save_store(d):
    try:
        os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)
        with open(STORE_FILE, 'w') as f:
            json.dump(d, f)
    except Exception:
        logger.exception('save_store failed')

def load_store():
    try:
        if os.path.exists(STORE_FILE):
            return json.load(open(STORE_FILE))
    except Exception:
        logger.exception('load_store failed')
    return {}

# ---------- Termux helpers ----------
def termux_battery():
    out = run_cmd('termux-battery-status')
    try:
        return json.loads(out)
    except Exception:
        return {'raw': out}

def termux_location():
    out = run_cmd('termux-location -p gps,network -r 5')
    try:
        return json.loads(out)
    except Exception:
        return {'raw': out}

def termux_play_alarm():
    if os.path.exists(ALARM_FILE):
        return run_cmd(f'termux-media-player play {ALARM_FILE}')
    else:
        return run_cmd("termux-notification -t 'Alarm' -c 'Alarm triggered'")

def termux_take_photo(out_path, camera=0):
    return run_cmd(f'termux-camera-photo -c {camera} {out_path}', timeout=25)

# ---------- Auth ----------
def check_auth(update, args):
    chat_id = update.effective_chat.id
    if ADMIN_CHAT_ID is not None:
        try:
            if int(chat_id) != int(ADMIN_CHAT_ID):
                return False, 'Access denied.'
        except Exception:
            return False, 'Access denied.'
    if not args or args[0] != PASSWORD:
        return False, 'Wrong or missing password.'
    return True, ''

# ---------- Utility features ----------
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

# ---------- Commands ----------
from telegram import ParseMode

def cmd_start(update, context):
    update.message.reply_text('Anti-Theft bot active. Use /help')

def cmd_help(update, context):
    update.message.reply_text(
        '/status <password>\n/loc <password>\n/alarm <password>\n/lock <password>\n/photo <password> [front/back]\n/sethome <password> <lat> <lon>\n/geostatus <password>\n/ping <password>'
    )

def cmd_status(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason)
        return
    batt = termux_battery()
    ip = requests.get('https://api.ipify.org').text if True else 'N/A'
    model = run_cmd('getprop ro.product.model')
    android_ver = run_cmd('getprop ro.build.version.release')
    text = (
        f'*Device Status*\nModel: `{model}`\nAndroid: `{android_ver}`\n'
        f'Battery: `{batt.get("percentage","N/A")}`%\nIP: `{ip}`\n'
    )
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f'STATUS by {update.effective_chat.id}')

def cmd_loc(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    loc = termux_location()
    if isinstance(loc, dict) and loc.get('latitude'):
        lat = loc.get('latitude'); lon = loc.get('longitude'); acc = loc.get('accuracy','N/A')
        maps = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}'
        update.message.reply_text(f'Lat:`{lat}`\nLon:`{lon}`\nAcc:`{acc}`\n{maps}', parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(f'Location failed: `{str(loc)[:400]}`', parse_mode=ParseMode.MARKDOWN)

def cmd_alarm(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    update.message.reply_text('Alarm triggered.')
    termux_play_alarm()

def cmd_lock(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    out = run_cmd('input keyevent 26')
    update.message.reply_text(f'Lock attempted. result:`{out}`', parse_mode=ParseMode.MARKDOWN)

def cmd_photo(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    camera = 0
    if len(context.args) >= 2 and context.args[1].lower().startswith('back'):
        camera = 1
    out_path = os.path.expanduser('~/Advanced-AntiTheft-Bot/last_photo.jpg')
    update.message.reply_text('Taking photo (may prompt permission)...')
    res = termux_take_photo(out_path, camera=camera)
    if os.path.exists(out_path):
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(out_path,'rb'))
            update.message.reply_text('Photo sent.')
        except Exception as e:
            update.message.reply_text(f'Error sending photo: {e}')
    else:
        update.message.reply_text(f'Photo capture failed: {res}')

def cmd_sethome(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    if len(context.args) < 3:
        update.message.reply_text('Usage: /sethome <password> <lat> <lon>')
        return
    try:
        lat = float(context.args[1]); lon = float(context.args[2])
        store = load_store()
        store['home'] = {'lat': lat, 'lon': lon, 'radius': GEOFENCE_RADIUS_M}
        save_store(store)
        update.message.reply_text(f'Home set: {lat},{lon} radius {GEOFENCE_RADIUS_M}m')
    except Exception as e:
        update.message.reply_text(f'Parse error: {e}')

def cmd_geostatus(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    store = load_store(); home = store.get('home')
    if not home:
        update.message.reply_text('Home not set. Use /sethome'); return
    loc = termux_location()
    if isinstance(loc, dict) and loc.get('latitude'):
        lat=loc.get('latitude'); lon=loc.get('longitude')
        d = haversine(lat, lon, home['lat'], home['lon'])
        inside = d <= home.get('radius', GEOFENCE_RADIUS_M)
        update.message.reply_text(f'Distance to home: {int(d)} m. Inside: {inside}')
    else:
        update.message.reply_text('Could not fetch location.')

def cmd_ping(update, context):
    ok, reason = check_auth(update, context.args)
    if not ok:
        update.message.reply_text(reason); return
    update.message.reply_text('PONG')

def cmd_store(update, context):
    if ADMIN_CHAT_ID is not None and int(update.effective_chat.id)!=int(ADMIN_CHAT_ID):
        return
    store = load_store(); update.message.reply_text(f"Store: `{json.dumps(store)[:1200]}`", parse_mode=ParseMode.MARKDOWN)

# ---------- Heartbeat thread ----------

def heartbeat_loop(updater):
    if HEARTBEAT_MIN <= 0:
        logger.info('Heartbeat disabled')
        return
    bot = updater.bot
    while True:
        try:
            store = load_store(); admin = ADMIN_CHAT_ID
            if admin:
                batt = termux_battery(); ip = requests.get('https://api.ipify.org').text
                msg = f"[HEARTBEAT]\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nBattery: {batt.get('percentage','N/A')}%\nIP: {ip}"
                bot.send_message(chat_id=admin, text=msg)
                home = store.get('home')
                if home:
                    loc = termux_location()
                    if isinstance(loc, dict) and loc.get('latitude'):
                        lat=loc.get('latitude'); lon=loc.get('longitude')
                        d = haversine(lat, lon, home['lat'], home['lon'])
                        if d > home.get('radius', GEOFENCE_RADIUS_M):
                            bot.send_message(chat_id=admin, text=f"[GEO ALERT] Device is {int(d)}m away from home center.")
            else:
                logger.debug('Heartbeat: no ADMIN_CHAT_ID set.')
        except Exception:
            logger.exception('Heartbeat loop error')
        time.sleep(HEARTBEAT_MIN * 60)

# ---------- SIM check ----------
def termux_get_sim_serial():
    return run_cmd('getprop gsm.sim.operator.alpha || getprop ril.serialnumber')

def check_sim_change(updater):
    try:
        current = termux_get_sim_serial(); store = load_store(); last = store.get('sim_serial')
        if last and last != current:
            admin = ADMIN_CHAT_ID
            if admin:
                updater.bot.send_message(chat_id=admin, text=f"[SIM CHANGE] previous: `{last}` new: `{current}`")
        store['sim_serial'] = current; save_store(store)
    except Exception:
        logger.exception('SIM check failed')

# ---------- Auto-update (safe) ----------
def auto_update_from_github():
    if not AUTO_UPDATE or not GITHUB_REPO:
        return
    try:
        # do a git pull in repo dir if exists
        repo_dir = os.path.expanduser('~/Advanced-AntiTheft-Bot')
        if os.path.exists(repo_dir) and os.path.isdir(repo_dir):
            out = run_cmd(f'cd {repo_dir} && git pull')
            logger.info(f'Auto-update: {out}')
    except Exception:
        logger.exception('Auto-update failed')

# ---------- Main ----------
def main():
    if not BOT_TOKEN or BOT_TOKEN.startswith('PUT_YOUR'):
        print('Please edit config.json with BOT_TOKEN and PASSWORD')
        return
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', cmd_start))
    dp.add_handler(CommandHandler('help', cmd_help))
    dp.add_handler(CommandHandler('status', cmd_status, pass_args=True))
    dp.add_handler(CommandHandler('loc', cmd_loc, pass_args=True))
    dp.add_handler(CommandHandler('alarm', cmd_alarm, pass_args=True))
    dp.add_handler(CommandHandler('lock', cmd_lock, pass_args=True))
    dp.add_handler(CommandHandler('photo', cmd_photo, pass_args=True))
    dp.add_handler(CommandHandler('sethome', cmd_sethome, pass_args=True))
    dp.add_handler(CommandHandler('geostatus', cmd_geostatus, pass_args=True))
    dp.add_handler(CommandHandler('ping', cmd_ping, pass_args=True))
    dp.add_handler(CommandHandler('store', cmd_store))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda u,c: c.bot.send_message(chat_id=u.effective_chat.id, text='Got your message.') if (ADMIN_CHAT_ID is None or int(u.effective_chat.id)==int(ADMIN_CHAT_ID)) else None))

    updater.start_polling()
    logger.info('Bot started')

    # sim check
    try:
        check_sim_change(updater)
    except Exception:
        logger.exception('SIM check exception')

    # heartbeat
    if HEARTBEAT_MIN > 0 and ADMIN_CHAT_ID:
        t = threading.Thread(target=heartbeat_loop, args=(updater,), daemon=True)
        t.start()

    # auto-update once at start
    threading.Thread(target=auto_update_from_github, daemon=True).start()

    updater.idle()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Fatal error')
