import threading
import os
import random
import logging
import sys
import time
from typing import List

# --- Standart ve Profesyonel Loglama Yapılandırması ---
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MainSystem")

# --- Yerel Modüller ---
from loader import bot
from server import start_uptime_server
from live_checker import start_live_stream_monitor
from utils import log
from config import HEDEF_KANAL

# Handler modülleri bot objesini import edip kaydettikleri için burada çağrılmaları yeterlidir
import moderation
import commands


class GizzyBotApplication:
    """Botun ana döngüsünü, thread'lerini ve yaşam döngüsünü yöneten çekirdek sınıf."""
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.announce_file = 'oto_duyuru.txt'
        self.announce_interval = 3600  # Saniye (1 Saat)
        self.target_channel = self._format_channel_name(HEDEF_KANAL)
        self._print_banner()

    @staticmethod
    def _print_banner() -> None:
        """Terminal başlangıç görselini basar."""
        banner = """
        ============================================================
        💎 GIZZY EXECUTIVE TELEGRAM ASSISTANT BOT STARTING... 💎
        ============================================================
        """
        print(banner)

    @staticmethod
    def _format_channel_name(channel: str) -> str:
        """Kanal adını sadece bir kez valide eder ve formatlar."""
        channel_str = str(channel).strip()
        if not channel_str:
            logger.error("HEDEF_KANAL tanımsız veya boş! Fallback çalışıyor.")
            return "@gizzy_kanal_varsayilan" # Hata anında çökmeyi engellemek için
        return f"@{channel_str}" if not channel_str.startswith("@") else channel_str

    def _read_announcements(self) -> List[str]:
        """Duyuru dosyasını güvenli bir şekilde okur."""
        if not os.path.exists(self.announce_file):
            logger.warning(f"{self.announce_file} bulunamadı.")
            return []

        try:
            # Sadece 1MB'a kadar olan dosyaları okuyarak bellek taşmasını önleriz
            if os.path.getsize(self.announce_file) > 1024 * 1024:
                logger.error("Duyuru dosyası 1MB'dan büyük! Güvenlik gereği okunmadı.")
                return []

            with open(self.announce_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Dosya okuma hatası: {e}")
            return []

    def oto_duyuru_gonder(self) -> None:
        """Belirlenen aralıklarla hedef kanala duyuru atan thread motoru."""
        # Bot başladığında ilk duyuruyu atmak için kısa bir başlangıç süresi (15 sn)
        self.stop_event.wait(15) 
        
        while not self.stop_event.is_set():
            mesajlar = self._read_announcements()
            
            if mesajlar:
                try:
                    rastgele_mesaj = random.choice(mesajlar)
                    mesaj_metni = f"📢 <b>Hatırlatma:</b>\n\n{rastgele_mesaj}"
                    
                    bot.send_message(
                        chat_id=self.target_channel, 
                        text=mesaj_metni, 
                        parse_mode='HTML'
                    )
                    logger.info(f"Duyuru gönderildi: {self.target_channel}")
                    log("📣 Otomatik duyuru gruba başarıyla gönderildi.") # Geriye dönük uyumluluk
                except Exception as e:
                    logger.error(f"Duyuru gönderiminde ağ/API hatası: {e}")
            else:
                logger.debug("Gönderilecek geçerli duyuru bulunamadı.")

            # time.sleep yerine event tabanlı bekleme. Bot kapanırsa anında kırılır.
            self.stop_event.wait(self.announce_interval)

    def start_background_services(self) -> None:
        """Tüm arka plan servislerini izole edilmiş Thread'ler içinde başlatır."""
        
        # 1. Uptime Server (Web Sunucusu bloklamasını engellemek için thread içine aldık)
        logger.info("🌐 Web sunucusu iş parçacığı başlatılıyor...")
        threading.Thread(
            target=start_uptime_server, 
            name="WebServer_Thread", 
            daemon=True
        ).start()

        # 2. Canlı Yayın Monitörü
        logger.info("🎥 Canlı yayın tarama motoru başlatılıyor...")
        threading.Thread(
            target=start_live_stream_monitor, 
            name="LiveMonitor_Thread", 
            daemon=True
        ).start()

        # 3. Otomatik Duyuru Sistemi
        logger.info(f"📢 Duyuru motoru başlatıldı (Aralık: {self.announce_interval}sn).")
        threading.Thread(
            target=self.oto_duyuru_gonder, 
            name="AutoAnnounce_Thread", 
            daemon=True
        ).start()

    def run_polling(self) -> None:
        """Telegram API bağlantısını sonsuz döngü ve hata kontrolü ile yönetir."""
        logger.info("🚀 Telegram API Polling başlatılıyor. Sistem aktif!")
        
        while not self.stop_event.is_set():
            try:
                bot.infinity_polling(timeout=20, long_polling_timeout=10, logger_level=logging.ERROR)
            except KeyboardInterrupt:
                break  # Manuel kapatma sinyali (Ctrl+C) geldiğinde döngüyü kır
            except Exception as e:
                logger.critical(f"❌ Kritik Polling Bağlantı Hatası: {e}")
                # Hata durumunda ardışık denemelerin CPU'yu boğmaması için event bazlı bekleme
                self.stop_event.wait(5)

    def shutdown(self) -> None:
        """Tüm alt süreçleri güvenli ve temiz bir şekilde kapatır."""
        logger.info("🛑 Kapatma sinyali alındı. Tüm iş parçacıkları durduruluyor...")
        self.stop_event.set()
        bot.stop_polling()
        logger.info("✅ Sistem güvenle kapatıldı.")
        sys.exit(0)


if __name__ == "__main__":
    app = GizzyBotApplication()
    try:
        app.start_background_services()
        app.run_polling()
    except KeyboardInterrupt:
        app.shutdown()
    except Exception as fatal_error:
        logger.critical(f"SİSTEM ÇÖKTÜ: {fatal_error}")
        app.shutdown()