import time
import requests
import os
from datetime import datetime
from config import KICK_CHANNEL, YOUTUBE_CHANNEL, HEDEF_KANAL, RESIM_YOLU
from loader import bot
from utils import log, load_stats, save_stats

def check_kick_live():
    try:
        url = f"https://kick.com/api/v1/channels/{KICK_CHANNEL}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json().get("livestream") is not None
    except Exception as e:
        log(f"Kick API bağlantı sorunu: {e}")
    return False

def check_youtube_live():
    try:
        url = f"https://www.youtube.com/@{YOUTUBE_CHANNEL}/live"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        return ("watch?v=" in r.url) or ("isLiveNow" in r.text)
    except Exception as e:
        log(f"YouTube Live tarama sorunu: {e}")
    return False

def start_live_stream_monitor():
    kick_was_live = False
    youtube_was_live = False
    tarama_sayaci = 1  # Sayaç başlangıcı

    kick_banner = (
        "🎰 <b>GIZZY KICK PLATFORMUNDA YAYINDA!</b> 🎰\n\n"
        "Büyük ödüller, muazzam heyecan ve kesintisiz eğlence başladı.\n"
        "Hemen masadaki yerini ayırt ve yayına ak!\n\n"
        "👉 <a href='https://kick.com/gizzykick'>CANLI YAYINA KATIL</a>"
    )

    youtube_banner = (
        "🔴 <b>GIZZY YOUTUBE EKRANLARINDA YAYINDA!</b> 🔴\n\n"
        "Canlı yayınımız YouTube platformunda an itibariyle aktiftir.\n"
        "Sohbete katılmak ve canlı izlemek için tıklayın!\n\n"
        "👉 <a href='https://youtube.com/@gizzylive2/streams'>YAYINA KATIL</a>"
    )

    while True:
        try:
            # 1. Platformların anlık durumunu kontrol et
            kick_is_live = check_kick_live()
            youtube_is_live = check_youtube_live()

            # 2. Terminale Log Düş (Senin İstediğin Özellik)
            kick_durum = "Açık 🟢" if kick_is_live else "Kapalı 🔴"
            yt_durum = "Açık 🟢" if youtube_is_live else "Kapalı 🔴"
            
            log(f"--- {tarama_sayaci}. Tarama --- | Kick: {kick_durum} | YouTube: {yt_durum}")
            tarama_sayaci += 1

            # 3. Kick Duyuru Mantığı
            if kick_is_live:
                if not kick_was_live:
                    stats = load_stats()
                    stats["toplam_yayin"] += 1
                    stats["son_yayin_tarihi"] = datetime.now().strftime("%d.%m.%Y %H:%M")
                    save_stats(stats)
                    
                    if os.path.exists(RESIM_YOLU):
                        with open(RESIM_YOLU, 'rb') as photo:
                            bot.send_photo(f"@{HEDEF_KANAL}", photo, caption=kick_banner, parse_mode='HTML')
                    else:
                        bot.send_message(f"@{HEDEF_KANAL}", kick_banner, parse_mode='HTML')
                    log("📣 Kick Yayın Duyurusu Başarıyla Gönderildi.")
                    kick_was_live = True
            else:
                kick_was_live = False

            # 4. YouTube Duyuru Mantığı
            if youtube_is_live:
                if not youtube_was_live:
                    if os.path.exists(RESIM_YOLU):
                        with open(RESIM_YOLU, 'rb') as photo:
                            bot.send_photo(f"@{HEDEF_KANAL}", photo, caption=youtube_banner, parse_mode='HTML')
                    else:
                        bot.send_message(f"@{HEDEF_KANAL}", youtube_banner, parse_mode='HTML')
                    log("📣 YouTube Yayın Duyurusu Başarıyla Gönderildi.")
                    youtube_was_live = True
            else:
                youtube_was_live = False

        except Exception as e:
            log(f"Yayın tarayıcı döngü hatası: {e}")

        # Her döngü sonu 60 saniye (1 dakika) bekler
        time.sleep(60)