from telebot import types
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import *

from telebot import util
bot = TeleBot(BOT_TOKEN, threaded=False)

hideBoard = types.ReplyKeyboardRemove()

# admin id chat
ADMIN_CHAT_ID = ""

# ChatAperta
ChatAperta = False

# IMAGELINK
immagine_scuola = "<a href=\"https://">\n🏞</a>"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"👋 {message.from_user.username}, sono il bot")

    text = f"Cosa vuoi fare? {immagine_scuola}"

    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=steamMarkup())

def steamMarkup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('📘 info', '🔗 social')
    markup.add('💬 parla con un admin',  '👨‍💻 developer')
    markup.add('❌ exit')
    return markup

@bot.message_handler(func=lambda m: True)
def any(message):
    forward_message(message)
    if 'info' in message.text:
        bot.reply_to(message, "")
    elif 'social' in message.text:
        bot.reply_to(message, "Puoi contattarci su \ninstagram \nfacebook \nwhatsapp.", reply_markup=step_markup())
    elif 'parla con un admin' in message.text:
        bot.reply_to(message, "Chat con admin", reply_markup=aspi_admin())
    elif 'developer' in message.text:
        bot.reply_to(message, "Il bot è stato creato dal nostro tecnico informatico @Step1992.")
    elif 'exit' in message.text:
        bot.reply_to(message, "Ciao 👋, hai chiuso il bot per farlo funzionare digita /start.", reply_markup=types.ReplyKeyboardRemove())

def step_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Instagram", url="https://www.instagram.com/"),
               InlineKeyboardButton("Whatsapp", url="https://wa.me/"))
    markup.add(InlineKeyboardButton("Facebook", url="https://www.facebook.com/"),
               InlineKeyboardButton("Pagina Facebook", url="https://www.facebook.com/"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global ChatAperta
    chat_id = call.message.chat.id
    if call.data == 'open_chat':
        ChatAperta = True
        bot.send_message(chat_id, "Hai avviato una chat privata con un amministratore. Scrivi il tuo messaggio:")
        bot.register_next_step_handler(call.message, forward_to_admin)
    elif call.data == 'close_chat':
        ChatAperta = False
        bot.send_message(chat_id, "Hai chiuso la chat con l'amministratore.", reply_markup=steamMarkup())

def forward_to_admin(message):
    admin_chat_id = ADMIN_CHAT_ID
    user_chat_id = message.chat.id
    text = f"Messaggio da {message.chat.first_name} ({user_chat_id}): {message.text}"
    admin_msg = bot.send_message(admin_chat_id, text)
    bot.register_next_step_handler(admin_msg, forward_to_user, user_chat_id)

def forward_message(message):
    if ChatAperta:
        admin_chat_id = ADMIN_CHAT_ID
        user_chat_id = message.chat.id
        text = f"Messaggio da {message.chat.first_name} ({user_chat_id}): {message.text}"
        admin_msg = bot.send_message(admin_chat_id, text)
        bot.register_next_step_handler(admin_msg, forward_to_user, user_chat_id)

def forward_to_user(admin_msg, user_chat_id):
    if ChatAperta:
        text = f"Risposta da un amministratore: {admin_msg.text}"
        bot.send_message(user_chat_id, text)

def aspi_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔓 Apri chat", callback_data="open_chat"),
               InlineKeyboardButton("🔒 Chiudi chat", callback_data="close_chat"))
    return markup

print('Il bot è attivo')
bot.infinity_polling()
