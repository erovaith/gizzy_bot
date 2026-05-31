import os

# Telegram Bot Token
BOT_TOKEN = "8909397616:AAHsnzQrhm0n-g9KLL6ewH0GMcUtBNZB7EA"

# Kanal ve Grup Kullanıcı Adları (Başında @ olmadan yazın)
HEDEF_KANAL = "gizzysohbet"
KAYNAK_KANAL = "betifaguncel"

# Sosyal Medya ve Yayın Platformu Kullanıcı Adları
KICK_CHANNEL = "gizzykick"
YOUTUBE_CHANNEL = "gizzylive2"
INSTAGRAM = "qiizzeemm_"

# Dosya Yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESIM_YOLU = os.path.join(BASE_DIR, "image.jpg")
STATS_FILE = os.path.join(BASE_DIR, "stats.json")
KUFUR_DOSYASI = os.path.join(BASE_DIR, "kufurler.txt")

# Filtre Ayarları
LINKLER = ['http://', 'https://', 'www.', '.com', '.net', '.org', '.xyz', 't.me/', 'amzn.to', 'bi.link']