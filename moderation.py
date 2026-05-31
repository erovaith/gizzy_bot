import telebot
import threading
from loader import bot
from config import HEDEF_KANAL, KAYNAK_KANAL, LINKLER
from utils import load_kufurler, is_admin, log, safe_delete_message

KUFUR_LISTESI = load_kufurler()

# --- Yeni Katılanları Karşılama ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for member in message.new_chat_members:
        hosgeldin_metni = (
            f"👋 <b>Aramıza hoş geldin, {member.first_name}!</b>\n\n"
            f"🎰 Gizzy topluluğuna katıldın. Burada yayın bildirimleri, eğlence ve harika bir sohbet var.\n\n"
            f"⚠️ Lütfen grupta aktif olmadan önce <b>/kurallar</b> komutunu okumayı unutma.\n"
            f"🤖 Bot komutlarını listelemek için <b>/yardim</b> yazabilirsin."
        )
        msg = bot.send_message(message.chat.id, hosgeldin_metni, parse_mode='HTML')
        
        # Karşılama mesajı kalabalık yapmasın diye 30 saniye sonra otomatik silinir
        def auto_delete_welcome():
            import time
            time.sleep(30)
            safe_delete_message(message.chat.id, msg.message_id)
        threading.Thread(target=auto_delete_welcome, daemon=True).start()

# --- Admin Moderasyon Komutları (/ban, /mute, /unban, /unmute) ---
@bot.message_handler(commands=['ban', 'unban', 'mute', 'unmute'])
def admin_actions(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "⚠️ Bu komut yalnızca grup yöneticileri (Admin) içindir.")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Bu komutu kullanmak için cezalandırılacak kişinin mesajını yanıtlamalısınız.")
        return

    target_user = message.reply_to_message.from_user
    command = message.text.split()[0].lower()

    try:
        if command == '/ban':
            bot.ban_chat_member(message.chat.id, target_user.id)
            bot.send_message(message.chat.id, f"🔨 <b>{target_user.first_name}</b> gruptan kalıcı olarak uzaklaştırıldı.", parse_mode='HTML')
        elif command == '/unban':
            bot.unban_chat_member(message.chat.id, target_user.id)
            bot.send_message(message.chat.id, f"✅ <b>{target_user.first_name}</b> ceza kilidi kaldırıldı.", parse_mode='HTML')
        elif command == '/mute':
            bot.restrict_chat_member(message.chat.id, target_user.id, can_send_messages=False)
            bot.send_message(message.chat.id, f"🔇 <b>{target_user.first_name}</b> süresiz olarak susturuldu.", parse_mode='HTML')
        elif command == '/unmute':
            bot.restrict_chat_member(message.chat.id, target_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
            bot.send_message(message.chat.id, f"🔊 <b>{target_user.first_name}</b> konuşma izni geri verildi.", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Yetki yetersiz veya Telegram API hatası: {e}")

# --- Mesaj Temizleme Komutu (/temizle) ---
@bot.message_handler(commands=['temizle'])
def clear_messages(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return
    try:
        args = message.text.split()
        count = int(args[1]) if len(args) > 1 else 10
        if count > 100: count = 100  # Telegram sınırlandırması için limit
        
        current_id = message.message_id
        deleted = 0
        for i in range(count + 1):
            try:
                bot.delete_message(message.chat.id, current_id - i)
                deleted += 1
            except:
                pass
        
        info = bot.send_message(message.chat.id, f"🧹 Başarıyla son {deleted - 1} mesaj gruptan temizlendi.")
        def del_info():
            import time
            time.sleep(5)
            safe_delete_message(message.chat.id, info.message_id)
        threading.Thread(target=del_info, daemon=True).start()
    except Exception as e:
        bot.reply_to(message, "⚠️ Doğru kullanım: `/temizle 20` (Sadece sayı girin)")

# Başında '/' olan komutları filtreleme ki commands.py çalışabilsin!
@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
def chat_filter_and_reply(message):
    text_lower = message.text.lower()
    words = text_lower.split()
    user_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    
    # Mesaj gruptan mı geliyor yoksa bota özelden (DM) mi atılmış kontrol et
    is_target_group = message.chat.username and message.chat.username.lower() == HEDEF_KANAL.lower()
    is_private_chat = message.chat.type == 'private'

    # Eğer mesaj hedef gruptan veya özel DM'den gelmiyorsa (başka yabancı bir gruptaysa) işlem yapma
    if not (is_target_group or is_private_chat):
        return

    admin_status = is_admin(message.chat.id, message.from_user.id) if not is_private_chat else False

    # 1. Aşama: Küfür Filtresi (Sadece Gruplarda Çalışsın, Özelde Engellemesin)
    if not is_private_chat and (any(k in words for k in KUFUR_LISTESI) or any(k in text_lower for k in ['siktir', 'oroppu', 'amına'])):
        safe_delete_message(message.chat.id, message.message_id)
        warning = bot.send_message(message.chat.id, f"⚠️ {user_display}, <b>grupta küfürlü/argo terimlerin kullanımı kesinlikle yasaktır!</b> Mesajın silindi.", parse_mode='HTML')
        def del_warn():
            import time
            time.sleep(5)
            safe_delete_message(message.chat.id, warning.message_id)
        threading.Thread(target=del_warn, daemon=True).start()
        log(f"🚫 Küfür Filtresi: {user_display} mesajı engellendi.")
        return

    # 2. Aşama: Link Filtresi (Sadece Gruplarda ve Admin Olmayanlar İçin)
    if not is_private_chat and not admin_status and any(link in text_lower for link in LINKLER):
        safe_delete_message(message.chat.id, message.message_id)
        warning = bot.send_message(message.chat.id, f"🚫 {user_display}, <b>bu grupta reklam veya dış bağlantı (link) paylaşımı yasaktır!</b>", parse_mode='HTML')
        def del_warn():
            import time
            time.sleep(5)
            safe_delete_message(message.chat.id, warning.message_id)
        threading.Thread(target=del_warn, daemon=True).start()
        log(f"🚫 Link Filtresi: {user_display} bağlantı paylaşımı engellendi.")
        return

    # 3. Aşama: Akıllı Sohbet Cevapları (Hem grupta hem özel DM'de çalışır)
    if text_lower in ['sa', 's.a', 'selam', 'selamun aleyküm', 'selamun aleykum', 'merhaba', 'mrb']:
        bot.reply_to(message, "Aleykümselam, masaya hoş geldin! Şansın bol olsun. 🎰")
    elif text_lower in ['nbr', 'naber', 'nasılsın', 'nasilsin']:
        bot.reply_to(message, "Harikayız! Yayın hazırlıkları tam gaz devam, seni sormalı? 🚀")

# --- Kaynak Kanaldan Mesaj Kopyalama Duvarı ---
@bot.message_handler(func=lambda m: m.chat.username and m.chat.username.lower() == KAYNAK_KANAL.lower())
def auto_copy_partner_messages(message):
    try:
        bot.copy_message(chat_id=f"@{HEDEF_KANAL}", from_chat_id=message.chat.id, message_id=message.message_id)
        log("🔥 Sponsor mesajı hedef gruba başarıyla kopyalandı.")
    except Exception as e:
        log(f"Kopyalama esnasında hata: {e}")