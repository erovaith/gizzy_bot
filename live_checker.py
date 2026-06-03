import time
import requests
import os
import logging
from datetime import datetime

# Yerel Modüller
from config import KICK_CHANNEL, YOUTUBE_CHANNEL, HEDEF_KANAL, RESIM_YOLU
from loader import bot
from utils import load_stats, save_stats, log

# Kurumsal Loglama Yapılandırması
logger = logging.getLogger("LiveChecker")
logger.setLevel(logging.INFO)

# Sabitler (Constants)
CHECK_INTERVAL = 60  # Saniye cinsinden tarama aralığı
REQUEST_TIMEOUT = 10 # API yanıt bekleme süresi

KICK_BANNER = (
    "🎰 <b>GIZZY KICK PLATFORMUNDA YAYINDA!</b> 🎰\n\n"
    "Büyük ödüller, muazzam heyecan ve kesintisiz eğlence başladı.\n"
    "Hemen masadaki yerini ayırt ve yayına ak!\n\n"
    "👉 <a href='https://kick.com/gizzykick'>CANLI YAYINA KATIL</a>"
)

YOUTUBE_BANNER = (
    "🔴 <b>GIZZY YOUTUBE EKRANLARINDA YAYINDA!</b> 🔴\n\n"
    "Canlı yayınımız YouTube platformunda an itibariyle aktiftir.\n"
    "Sohbete katılmak ve canlı izlemek için tıklayın!\n\n"
    "👉 <a href='https://youtube.com/@gizzylive2/streams'>YAYINA KATIL</a>"
)

def _get_headers() -> dict:
    """API istekleri için güvenlik duvarlarını aşmaya yardımcı standart başlıklar üretir."""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html, application/xhtml+xml",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

def check_kick_live(session: requests.Session) -> bool:
    """Kick API'si üzerinden yayının açık olup olmadığını kontrol eder."""
    url = f"https://kick.com/api/v1/channels/{KICK_CHANNEL}"
    try:
        response = session.get(url, headers=_get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # 4xx ve 5xx hatalarını yakalar
        
        data = response.json()
        return data.get("livestream") is not None

    except requests.exceptions.HTTPError as e:
        if response.status_code in [401, 403]:
            logger.warning(f"Kick Cloudflare Koruması / Yetki Hatası (403/401). Tarayıcı modülü gerekebilir: {e}")
        else:
            logger.error(f"Kick HTTP Hatası: {e}")
    except ValueError:
        logger.error("Kick API yanıtı geçerli bir JSON değil.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Kick Ağına Bağlanılamadı: {e}")
    
    return False

def check_youtube_live(session: requests.Session) -> bool:
    """YouTube kanal sayfasını analiz ederek canlı yayını tespit eder."""
    url = f"https://www.youtube.com/@{YOUTUBE_CHANNEL}/live"
    try:
        response = session.get(url, headers=_get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        # YouTube için sayfa kaynağı kontrolü
        return ("watch?v=" in response.url) or ("isLiveNow" in response.text)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"YouTube Live tarama ağ sorunu: {e}")
    
    return False

def _duyuru_gonder(platform_adi: str, banner_metni: str, stats_guncelle: bool = False):
    """Platform bağımsız merkezi duyuru gönderme motoru."""
    hedef = f"@{HEDEF_KANAL}" if not str(HEDEF_KANAL).startswith("@") else HEDEF_KANAL

    try:
        # İstatistikleri sadece Kick için veya istenildiğinde güncelle
        if stats_guncelle:
            stats = load_stats()
            stats["toplam_yayin"] += 1
            stats["son_yayin_tarihi"] = datetime.now().strftime("%d.%m.%Y %H:%M")
            save_stats(stats)

        # Görsel varsa görselle, yoksa düz metinle gönder
        if os.path.exists(RESIM_YOLU):
            with open(RESIM_YOLU, 'rb') as photo:
                bot.send_photo(chat_id=hedef, photo=photo, caption=banner_metni, parse_mode='HTML')
        else:
            bot.send_message(chat_id=hedef, text=banner_metni, parse_mode='HTML')
            
        mesaj = f"📣 {platform_adi} Yayın Duyurusu Başarıyla Gönderildi."
        logger.info(mesaj)
        log(mesaj)  # Geriye dönük uyumluluk için

    except Exception as e:
        logger.critical(f"❌ {platform_adi} duyurusu gruba atılırken kritik hata: {e}")
        log(f"Kritik Hata - {platform_adi} Duyurusu: {e}")

def start_live_stream_monitor():
    """Arka planda kesintisiz çalışan ana yayın tarama döngüsü."""
    kick_was_live = False
    youtube_was_live = False
    tarama_sayaci = 1

    logger.info("🚀 Canlı Yayın Tarayıcı Motoru Başlatıldı.")

    # Tüm döngü boyunca aynı oturumu (Session) kullanarak CPU ve Network tasarrufu sağlıyoruz
    with requests.Session() as session:
        while True:
            try:
                # 1. API Kontrolleri (İzole edilmiş fonksiyonlar)
                kick_is_live = check_kick_live(session)
                youtube_is_live = check_youtube_live(session)

                # 2. Terminal Durum Raporlaması
                kick_durum = "Açık 🟢" if kick_is_live else "Kapalı 🔴"
                yt_durum = "Açık 🟢" if youtube_is_live else "Kapalı 🔴"
                
                rapor = f"--- {tarama_sayaci}. Tarama --- | Kick: {kick_durum} | YouTube: {yt_durum}"
                logger.info(rapor)
                log(rapor)  # Utils modülü uyumluluğu için
                
                tarama_sayaci += 1

                # 3. Kick Duyuru Karar Mekanizması
                if kick_is_live and not kick_was_live:
                    _duyuru_gonder(platform_adi="Kick", banner_metni=KICK_BANNER, stats_guncelle=True)
                    kick_was_live = True
                elif not kick_is_live:
                    kick_was_live = False

                # 4. YouTube Duyuru Karar Mekanizması
                if youtube_is_live and not youtube_was_live:
                    _duyuru_gonder(platform_adi="YouTube", banner_metni=YOUTUBE_BANNER, stats_guncelle=False)
                    youtube_was_live = True
                elif not youtube_is_live:
                    youtube_was_live = False

            except Exception as e:
                # Döngünün tamamen çökmesini engelleyen son kale
                logger.error(f"Yayın tarayıcı ana döngüsünde beklenmedik hata: {e}")

            # CPU'yu dinlendirme ve Rate-Limit'ten kaçınma
            time.sleep(CHECK_INTERVAL)