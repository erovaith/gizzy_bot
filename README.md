<<<<<<< HEAD
# 🚀 Gizzy Live & Moderasyon Telegram Botu

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Telebot](https://img.shields.io/badge/pyTelegramBotAPI-latest-green.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-red.svg?style=for-the-badge)
![Uptime](https://img.shields.io/badge/Uptime-7%2F24-brightgreen.svg?style=for-the-badge)

Yayıncılar, içerik üreticileri ve büyük topluluk grupları için Python ile geliştirilmiş **tam donanımlı, modüler ve 7/24 kesintisiz çalışabilen** profesyonel bir Telegram asistan ve moderasyon botudur.

## 🌟 Temel Özellikler

- **🔴 Otomatik Yayın Takibi:** Kick ve YouTube platformlarını eşzamanlı olarak arka planda tarar. Yayın başladığında belirlediğiniz banner görseli ve link ile gruba otomatik duyuru atar.
- **🛡️ Gelişmiş Moderasyon:** Özelleştirilebilir kelime/küfür filtresi ve yetkisiz link/reklam koruması. İhlal durumunda anında mesaj silme ve uyarı sistemi.
- **⚙️ Admin Yönetim Araçları:** Grup yöneticileri için hızlı yanıtlı `/ban`, `/unban`, `/mute`, `/unmute` ve `/temizle` (toplu mesaj silme) komutları.
- **🤖 Akıllı Oto-Yanıt ve Karşılama:** Belirli anahtar kelimelere (Selam, Naber vb.) doğal cevaplar verir, gruba yeni katılanları kurallarla birlikte karşılar.
- **🎮 Etkileşim ve Eğlence:** `/zar`, `/yazitura`, `/şans`, `/8ball` gibi etkileşim artırıcı grup oyunları.
- **⚡ 7/24 Aktif (Uptime):** İçerisinde barındırdığı dahili Flask sunucusu sayesinde Render, Railway vb. bulut sistemlerinde uyku moduna geçmeden aralıksız çalışır.

## 📂 Proje Mimarisi

Spagetti koddan uzak, tamamen modüler ve yönetilebilir bir dosya yapısı kullanılmıştır:

```text
📁 gizzy_bot/
│── 📄 main.py           # Ana tetikleyici ve motor
│── 📄 config.py         # Ayarlar, Token ve Platform linkleri
│── 📄 live_checker.py   # Kick & YouTube API tarama modülü
│── 📄 moderation.py     # Küfür, link engelleme ve admin komutları
│── 📄 commands.py       # Kullanıcı komutları ve eğlence
│── 📄 server.py         # 7/24 Flask Web Sunucusu
│── 📄 utils.py          # Yardımcı araçlar ve istatistik loglama
│── 📄 loader.py         # Bot merkez objesi
│── 📄 kufurler.txt      # Filtrelenecek kelimeler veritabanı
│── 📄 requirements.txt  # Gerekli kütüphaneler

📞 İletişim ve Destek
Bu projenin geliştiricisi ile iletişime geçmek, geri bildirimde bulunmak veya özel yazılım projeleriniz için aşağıdaki kanalları kullanabilirsiniz:

📧 E-Posta: eroglumehmet910@hotmail.com

=======
# 🚀 Gizzy Live & Moderasyon Telegram Botu

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Telebot](https://img.shields.io/badge/pyTelegramBotAPI-latest-green.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-red.svg?style=for-the-badge)
![Uptime](https://img.shields.io/badge/Uptime-7%2F24-brightgreen.svg?style=for-the-badge)

Yayıncılar, içerik üreticileri ve büyük topluluk grupları için Python ile geliştirilmiş **tam donanımlı, modüler ve 7/24 kesintisiz çalışabilen** profesyonel bir Telegram asistan ve moderasyon botudur.

## 🌟 Temel Özellikler

- **🔴 Otomatik Yayın Takibi:** Kick ve YouTube platformlarını eşzamanlı olarak arka planda tarar. Yayın başladığında belirlediğiniz banner görseli ve link ile gruba otomatik duyuru atar.
- **🛡️ Gelişmiş Moderasyon:** Özelleştirilebilir kelime/küfür filtresi ve yetkisiz link/reklam koruması. İhlal durumunda anında mesaj silme ve uyarı sistemi.
- **⚙️ Admin Yönetim Araçları:** Grup yöneticileri için hızlı yanıtlı `/ban`, `/unban`, `/mute`, `/unmute` ve `/temizle` (toplu mesaj silme) komutları.
- **🤖 Akıllı Oto-Yanıt ve Karşılama:** Belirli anahtar kelimelere (Selam, Naber vb.) doğal cevaplar verir, gruba yeni katılanları kurallarla birlikte karşılar.
- **🎮 Etkileşim ve Eğlence:** `/zar`, `/yazitura`, `/şans`, `/8ball` gibi etkileşim artırıcı grup oyunları.
- **⚡ 7/24 Aktif (Uptime):** İçerisinde barındırdığı dahili Flask sunucusu sayesinde Render, Railway vb. bulut sistemlerinde uyku moduna geçmeden aralıksız çalışır.

## 📂 Proje Mimarisi

Spagetti koddan uzak, tamamen modüler ve yönetilebilir bir dosya yapısı kullanılmıştır:

```text
📁 gizzy_bot/
│── 📄 main.py           # Ana tetikleyici ve motor
│── 📄 config.py         # Ayarlar, Token ve Platform linkleri
│── 📄 live_checker.py   # Kick & YouTube API tarama modülü
│── 📄 moderation.py     # Küfür, link engelleme ve admin komutları
│── 📄 commands.py       # Kullanıcı komutları ve eğlence
│── 📄 server.py         # 7/24 Flask Web Sunucusu
│── 📄 utils.py          # Yardımcı araçlar ve istatistik loglama
│── 📄 loader.py         # Bot merkez objesi
│── 📄 kufurler.txt      # Filtrelenecek kelimeler veritabanı
│── 📄 requirements.txt  # Gerekli kütüphaneler

📞 İletişim ve Destek
Bu projenin geliştiricisi ile iletişime geçmek, geri bildirimde bulunmak veya özel yazılım projeleriniz için aşağıdaki kanalları kullanabilirsiniz:

📧 E-Posta: eroglumehmet910@hotmail.com

>>>>>>> 6bcdebacff28f88584d73c641dc293c985bedf9f
Bu proje Mehmet Eroğlu tarafından ❤️ ile kodlanmıştır.