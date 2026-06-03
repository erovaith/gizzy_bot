<<<<<<< HEAD
import os
import json
import threading
import time
from datetime import datetime
from config import STATS_FILE, KUFUR_DOSYASI, HEDEF_KANAL
from loader import bot

def get_log_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    print(f"[{get_log_time()}] ℹ️ {msg}", flush=True)

def load_kufurler():
    if not os.path.exists(KUFUR_DOSYASI):
        log("⚠️ KRİTİK HATA: kufurler.txt bulunamadı!")
        return []
    with open(KUFUR_DOSYASI, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_stats():
    if not os.path.exists(STATS_FILE):
        default_stats = {"toplam_yayin": 0, "toplam_sure": 0, "son_yayin_tarihi": "Henüz yayın taranmadı"}
        save_stats(default_stats)
        return default_stats
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"toplam_yayin": 0, "toplam_sure": 0, "son_yayin_tarihi": "Veri Hatası"}

def save_stats(data):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except Exception as e:
        log(f"Admin kontrol hatası: {e}")
        return False

def safe_delete_message(chat_id, msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except:
        pass

def schedule_message_deletion(chat_id, user_msg_id, bot_msg_id, delay):
    """Belirtilen saniye sonra hem kullanıcının komutunu hem de botun yanıtını siler."""
    def delayed_delete():
        time.sleep(delay)
        safe_delete_message(chat_id, user_msg_id)
        safe_delete_message(chat_id, bot_msg_id)
    
=======
import os
import json
import threading
import time
from datetime import datetime
from config import STATS_FILE, KUFUR_DOSYASI, HEDEF_KANAL
from loader import bot

def get_log_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    print(f"[{get_log_time()}] ℹ️ {msg}", flush=True)

def load_kufurler():
    if not os.path.exists(KUFUR_DOSYASI):
        log("⚠️ KRİTİK HATA: kufurler.txt bulunamadı!")
        return []
    with open(KUFUR_DOSYASI, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_stats():
    if not os.path.exists(STATS_FILE):
        default_stats = {"toplam_yayin": 0, "toplam_sure": 0, "son_yayin_tarihi": "Henüz yayın taranmadı"}
        save_stats(default_stats)
        return default_stats
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"toplam_yayin": 0, "toplam_sure": 0, "son_yayin_tarihi": "Veri Hatası"}

def save_stats(data):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except Exception as e:
        log(f"Admin kontrol hatası: {e}")
        return False

def safe_delete_message(chat_id, msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except:
        pass

def schedule_message_deletion(chat_id, user_msg_id, bot_msg_id, delay):
    """Belirtilen saniye sonra hem kullanıcının komutunu hem de botun yanıtını siler."""
    def delayed_delete():
        time.sleep(delay)
        safe_delete_message(chat_id, user_msg_id)
        safe_delete_message(chat_id, bot_msg_id)
    
>>>>>>> 6bcdebacff28f88584d73c641dc293c985bedf9f
    threading.Thread(target=delayed_delete, daemon=True).start()