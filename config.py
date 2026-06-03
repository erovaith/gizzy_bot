import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler (Lokalde çalışırken gerekli)
load_dotenv()

# Telegram Bot Token (Hassas Bilgi)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot token kontrolü
if not BOT_TOKEN:
    raise ValueError("HATA: BOT_TOKEN bulunamadı! Lütfen Render veya .env ayarlarını kontrol et.")

# Kanal ve Grup Kullanıcı Adları (Çevresel değişkenlerden okunuyor)
HEDEF_KANAL = os.getenv("HEDEF_KANAL")
KAYNAK_KANAL = os.getenv("KAYNAK_KANAL")

# Sosyal Medya ve Yayın Platformu Kullanıcı Adları
KICK_CHANNEL = os.getenv("KICK_CHANNEL")
YOUTUBE_CHANNEL = os.getenv("YOUTUBE_CHANNEL")
INSTAGRAM = os.getenv("INSTAGRAM")

# Dosya Yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESIM_YOLU = os.path.join(BASE_DIR, "image.jpg")
STATS_FILE = os.path.join(BASE_DIR, "stats.json")
KUFUR_DOSYASI = os.path.join(BASE_DIR, "kufurler.txt")

# Filtre Ayarları
LINKLER = ['http://', 'https://', 'www.', '.com', '.net', '.org', '.xyz', 't.me/', 'amzn.to', 'bi.link']