import os
import telebot

# Укажите токен вашего бота
TOKEN = '6570001717:AAGkraZGvw0lJTkwHPmSD0Y8_tM_bEIRcRc'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Функция для поиска треков с определенным исполнителем
def find_tracks_by_artist(artist):
    # Получаем путь к текущей директории
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Проверяем, что директория существует
    if os.path.exists(dir_path):
        # Получаем список файлов в текущей директории
        files = os.listdir(dir_path)
        
        # Создаем список для хранения треков с указанным исполнителем
        tracks = []
        
        # Ищем треки с заданным исполнителем
        for file in files:
            if artist.lower() in file.lower():
                tracks.append(file)
        
        return tracks
    return None

# Обработчик команды /tracks
@bot.message_handler(commands=['tracks'])
def handle_tracks_command(message):
    # Получаем исполнителя из сообщения пользователя
    artist = message.text.split(maxsplit=1)[1]
    
    # Ищем треки с указанным исполнителем
    tracks = find_tracks_by_artist(artist)
    
    # Проверяем, найдены ли треки
    if tracks:
        # Создаем клавиатуру с кнопками для каждого трека
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        for track in tracks:
            # Добавляем кнопку для каждого трека
            keyboard.add(telebot.types.InlineKeyboardButton(text=track, callback_data=track))
        
        # Отправляем пользователю сообщение с кнопками
        bot.send_message(message.chat.id, f"Найдено {len(tracks)} треков с исполнителем '{artist}':", reply_markup=keyboard)
    else:
        bot.reply_to(message, f"Треков с исполнителем '{artist}' не найдено")

# Обработчик нажатия на кнопку с названием трека
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Отправляем трек пользователю
    with open(call.data, 'rb') as audio:
        bot.send_audio(call.message.chat.id, audio)

# Запускаем бота
bot.polling()
