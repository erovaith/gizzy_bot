import random
from telebot import types
from loader import bot
from config import KICK_CHANNEL, YOUTUBE_CHANNEL, INSTAGRAM
from utils import load_stats, schedule_message_deletion, is_admin

# --- Sosyal Medya ve Hızlı Erişim Paneli (/site, /kick, /youtube, /sosyal, /izle) ---
@bot.message_handler(commands=['site', 'kick', 'youtube', 'sosyal', 'izle'])
def dynamic_links_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🟢 Gizzy Kick", url=f"https://kick.com/{KICK_CHANNEL}")
    btn2 = types.InlineKeyboardButton("🔴 Gizzy YouTube", url=f"https://youtube.com/@{YOUTUBE_CHANNEL}")
    btn3 = types.InlineKeyboardButton("🟣 Instagram", url=f"https://instagram.com/{INSTAGRAM}")
    btn4 = types.InlineKeyboardButton("👑 Betifa Resmi Partner", url="https://betifa.com")
    markup.add(btn1, btn2, btn3, btn4)

    panel_text = (
        "👑 <b>GIZZY LIVE RESMİ ERİŞİM PANELİ</b> 👑\n\n"
        "👉 Yayınlara katılmak, sponsor avantajlarından yararlanmak ve güncel bağlantılara ulaşmak için aşağıdaki butonları kullanabilirsiniz.\n\n"
        "<i>🌐 Ana sitemiz: gizzylive.com</i>"
    )
    
    msg = bot.reply_to(message, panel_text, reply_markup=markup, parse_mode='HTML')
    # Kullanıcı hiçbir şeye tıklamazsa 15 saniye sonra silinir
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)

# --- Yayın Bilgisi Komutu (/yayin) ---
@bot.message_handler(commands=['yayin'])
def stream_status(message):
    from live_checker import check_kick_live, check_youtube_live
    kick = check_kick_live()
    yt = check_youtube_live()
    
    if kick or yt:
        text = "🎮 <b>YAYIN DURUMU: AKTİF!</b>\n\n🔥 Şu an canlı yayındayız! Hemen masadaki yerini al kaçırma!"
    else:
        text = "😴 <b>YAYIN DURUMU: KAPALI</b>\n\nHer gün saat 22:00'da canlı yayındayız. Bildirimleri açmayı unutma!"
        
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)

# --- Son Yayın Komutu (/sonyayin) ---
@bot.message_handler(commands=['sonyayin'])
def last_stream(message):
    stats = load_stats()
    text = f"📅 <b>Son Başlatılan Yayın Tarihi:</b> {stats.get('son_yayin_tarihi', 'Kayıt Yok')}"
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)

# --- Yayın Programı Komutu (/program) ---
@bot.message_handler(commands=['program'])
def stream_schedule(message):
    text = "📅 <b>Haftalık Yayın Akış Bilgisi</b>\n\n⏰ Genellikle <b>her gün Türkiye saati ile 22:00'da</b> canlı yayınlarımız aktif olmaktadır. Sürpriz yayınlar gruptan duyurulur!"
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)

# --- Kurallar Komutu (/kurallar) ---
@bot.message_handler(commands=['kurallar'])
def community_rules(message):
    text = (
        "📜 <b>GIZZY SOHBET GRUP KURALLARI</b>\n\n"
        "1️⃣ Argo terim, küfür ve hakaret kullanımı koşulsuz ban sebebidir.\n"
        "2️⃣ Üyelerin özelden birbirini rahatsız etmesi reklam ve spam yapması yasaktır.\n"
        "3️⃣ Dini, milli ve siyasi hassas konuları tartışmaya açmak gruptan uzaklaştırılma nedenidir.\n"
        "4️⃣ Güvenliğiniz için grupta şahsi telefon veya hesap bilgilerinizi paylaşmayın."
    )
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 20)

# --- Adminleri Listeleme Komutu (/adminler) ---
@bot.message_handler(commands=['adminler'])
def list_admins(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        admin_list = "👑 <b>Grup Yönetim Kadrosu:</b>\n\n"
        for admin in admins:
            flag = "⭐" if admin.status == "creator" else "🛡️"
            name = admin.user.first_name
            user = f"@{admin.user.username}" if admin.user.username else "Gizli Profil"
            admin_list += f"{flag} {name} ({user})\n"
        msg = bot.reply_to(message, admin_list, parse_mode='HTML')
        schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)
    except:
        pass

# --- İstatistik Komutu (/istatistik) ---
@bot.message_handler(commands=['istatistik'])
def channel_stats(message):
    stats = load_stats()
    try:
        member_count = bot.get_chat_member_count(message.chat.id)
    except:
        member_count = "Bilinmiyor"
        
    text = (
        "📊 <b>KANAL VE BOT İSTATİSTİKLERİ</b>\n\n"
        f"🎰 Toplam Gerçekleşen Yayın: {stats.get('toplam_yayin', 0)}\n"
        f"👥 Gruptaki Toplam Üye: {member_count}\n"
        f"🤖 Bot Sürümü: v2.5 Premium\n"
        f"⚡ Sunucu Gecikmesi: Aktif & Stabil"
    )
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 15)

# --- Gelişmiş Çoklu Yardım Komutu Menüsü (/yardim, /help, /komutlar, /menu) ---
@bot.message_handler(commands=['yardim', 'help', 'komutlar', 'menu'])
def help_center(message):
    text = (
        "🤖 <b>GIZZY GELİŞMİŞ YARDIM MERKEZİ</b>\n\n"
        "🎰 <b>Yayın Odaklı Komutlar:</b>\n"
        "  └ `/yayin` - Güncel canlı yayın durumunu sorgular.\n"
        "  └ `/sonyayin` - Son yayının ne zaman açıldığını gösterir.\n"
        "  └ `/program` - Yayın günlerini ve standart saatleri listeler.\n"
        "  └ `/site` - Sosyal medya ve ana site paneline erişir.\n\n"
        "👑 <b>Topluluk & Bilgi:</b>\n"
        "  └ `/kurallar` - Topluluk sözleşmesini ve kuralları ekrana getirir.\n"
        "  └ `/adminler` - Gruptaki aktif yöneticileri listeler.\n"
        "  └ `/istatistik` - Genel veri sayaçlarını gösterir.\n\n"
        "🎮 <b>Eğlence & Aktivite:</b>\n"
        "  └ `/zar` - Gruba şans zarı fırlatır.\n"
        "  └ `/yazitura` - Yazı tura simülasyonu başlatır.\n"
        "  └ `/şans` - Günlük şans oranınızı hesaplar.\n"
        "  └ `/8ball` - Sihirli küreye soru sorarsınız."
    )
    msg = bot.reply_to(message, text, parse_mode='HTML')
    schedule_message_deletion(message.chat.id, message.message_id, msg.message_id, 25)

# --- EĞLENCE SİSTEMLERİ ---
@bot.message_handler(commands=['zar'])
def roll_dice(message):
    bot.send_dice(message.chat.id)

@bot.message_handler(commands=['yazitura'])
def coin_flip(message):
    choices = ["🪙 YAZI!", "🪙 TURA!", "🪙 Şans eseri dik geldi!"]
    bot.reply_to(message, f"Madeni para havaya fırlatıldı...\n\nSonuç: <b>{random.choice(choices)}</b>", parse_mode='HTML')

@bot.message_handler(commands=['şans'])
def luck_meter(message):
    rate = random.randint(1, 100)
    comment = "Bugün şansın zirvesindesin, masaya oturma vakti! 🎰" if rate > 75 else "Orta şekerli bir gün, kontrollü kal. ⚖️" if rate > 40 else "Bugün risk almasan iyi olur şef. 🚫"
    bot.reply_to(message, f"🍀 Günlük Şans Oranın: <b>%{rate}</b>\n\n📋 Analiz: <i>{comment}</i>", parse_mode='HTML')

@bot.message_handler(commands=['8ball'])
def magic_eight_ball(message):
    responses = ["Kesinlikle evet 🟢", "Büyük ihtimalle hayır 🔴", "Evren bu konuda kararsız görünüyor 🟡", "Buna güvenebilirsin ✔️", "Zaman harcamaya değmez ✖️"]
    bot.reply_to(message, f"🎱 Sihirli 8-Ball Cevaplıyor:\n\n💬 <i>\"{random.choice(responses)}\"</i>")