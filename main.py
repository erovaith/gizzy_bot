import threading
import time
from loader import bot
from server import start_uptime_server
from live_checker import start_live_stream_monitor
from utils import log

# Modüllerin Telegram üzerindeki handler (tetikleyicilerini) aktif etmek için import ediyoruz
import moderation
import commands

def init_system():
    print("="*60)
    print("💎 GIZZY EXECUTIVE TELEGRAM ASSISTANT BOT LOADED SUCCESSFULLY 💎")
    print("="*60)
    
    # 1. 7/24 Flask Web Sunucusunu Ateşle
    log("7/24 Web Sunucusu başlatılıyor...")
    start_uptime_server()
    
    # 2. Arka Plandaki Canlı Yayın Bildirim Motorunu Çalıştır
    log("Canlı yayın tarama motoru devreye alınıyor (Daemon)...")
    monitor_thread = threading.Thread(target=start_live_stream_monitor, daemon=True)
    monitor_thread.start()
    
    # 3. Telegram API Polling Başlat
    log("Telegram API Polling bağlantısı açılıyor...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            log(f"Sistem Polling Bağlantı Kaybı Yaşadı! 5 saniye sonra tekrar bağlanıyor... Hata: {e}")
            time.sleep(5)

if __name__ == "__main__":
    init_system()