import threading
import time
import os
import random
from loader import bot
from server import start_uptime_server
from live_checker import start_live_stream_monitor
from utils import log
from config import HEDEF_KANAL

# Modüller
import moderation
import commands

def oto_duyuru_gonder():
    """oto_duyuru.txt içinden rastgele duyuru seçip 1 saatte bir atar."""
    while True:
        time.sleep(1 * 3600)  # 1 Saat bekleme
        try:
            if os.path.exists('oto_duyuru.txt'):
                with open('oto_duyuru.txt', 'r', encoding='utf-8') as f:
                    mesajlar = f.readlines()
                
                if mesajlar:
                    rastgele_mesaj = random.choice(mesajlar).strip()
                    bot.send_message(f"@{HEDEF_KANAL}", f"📢 <b>Hatırlatma:</b>\n\n{rastgele_mesaj}", parse_mode='HTML')
                    log("📣 Otomatik duyuru gruba başarıyla gönderildi.")
        except Exception as e:
            log(f"Duyuru sistemi hatası: {e}")

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

    # 3. Otomatik Duyuru Sistemini Başlat
    log("Otomatik duyuru sistemi devrede (1 saatlik döngü)...")
    duyuru_thread = threading.Thread(target=oto_duyuru_gonder, daemon=True)
    duyuru_thread.start()
    
    # 4. Telegram API Polling Başlat
    log("Telegram API Polling bağlantısı açılıyor...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            log(f"Sistem Polling Bağlantı Kaybı Yaşadı! 5 saniye sonra tekrar bağlanıyor... Hata: {e}")
            time.sleep(5)

if __name__ == "__main__":
    init_system()