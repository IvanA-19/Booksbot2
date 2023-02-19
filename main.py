import telebot as t
import config
from telebot import types
from background import keep_alive

bot = t.TeleBot(config.token)

@bot.message_handler(content_types=['new_chat_members'])
def hello_member(message):
    user = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn = types.KeyboardButton('СТАРТ')
    markup.add(btn)
    bot.send_message(message.chat.id, text=f"Рад приветствовать, {user}! {config.txt}", reply_markup=markup)

@bot.message_handler(commands=['start'])
def st(message):
    bot.send_message(message.chat.id, text="Чтобы открыть меню бота используйте /menu")

@bot.message_handler(commands=['help'])
def help(message):
    text = config.txt2
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['menu'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Информация о произведениях')
    btn2 = types.KeyboardButton('Выбрать произведение')
    btn3 = types.KeyboardButton('Описание персонажей')
    markup.add(btn1, btn2, btn3)
    text = "Отлично! Теперь выберите, что вы хотите сделать)"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['Персонажи', 'characters'])
def characters(message):
    novels = ["Наше счастливое вчера", "Из мажоров в люди", "Какой же выбор сделать?", "Тени грешного города", "Повеси о пространстве и времени", "Пьеса об Иване и Юлианне"]
    items = []
    markup_inline = types.InlineKeyboardMarkup()
    for i in range(len(novels)):
        items.append(types.InlineKeyboardButton(text=novels[i], callback_data=f'novel{str(i)}'))
        markup_inline.add(items[i])
    bot.send_message(message.chat.id, 'Описание персонажей какого произведения вам интересно?', reply_markup=markup_inline)

@bot.message_handler(commands=['novels', 'О романах'])
def about_novels(message):
    novels = ["Наше счастливое вчера", "Из мажоров в люди", "Какой же выбор сделать?", "Тени грешного города", "Повести о пространстве и времени", "Пьеса об Иване и Юлианне"]
    items = []
    markup_inline = types.InlineKeyboardMarkup()
    for i in range(len(novels)):
        items.append(types.InlineKeyboardButton(text=novels[i], callback_data=f'novel_{str(i)}'))
        markup_inline.add(items[i])
    bot.send_message(message.chat.id, 'Описание какого произведения вы хотите прочитать?', reply_markup=markup_inline)

@bot.message_handler(commands=['author'])
def contact_information(message):
  bot.send_message(message.chat.id, text=config.txt3)

@bot.message_handler(content_types=['text'])
def start(message):
    rem = types.ReplyKeyboardRemove()
    if(message.text == 'Выбрать произведение'):
        markup_inline = types.InlineKeyboardMarkup()
        item_full = types.InlineKeyboardButton(text='Полное произведение', callback_data='full')
        item_certain = types.InlineKeyboardButton(text='Выбрать главу', callback_data='certain')
        markup_inline.add(item_full, item_certain)
        bot.send_message(message.chat.id, text="Выберите, что вы хотите: ", reply_markup=markup_inline)
    elif(message.text == 'Информация о произведениях'):
        bot.send_message(message.chat.id, text="Давайте выберем произведение)\nИспользуйте /novels или /О произведениях", reply_markup=rem)
    elif (message.text == 'Описание персонажей'):
        bot.send_message(message.chat.id, text="Давайте выберем произведение)\nИспользуйте /characters или /Персонажи", reply_markup=rem)
    elif(message.text == 'СТАРТ'):
        bot.send_message(message.chat.id, text="Чтобы открыть меню бота используйте /menu", reply_markup=rem)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    novels = ["Наше счастливое вчера", "Из мажоров в люди", "Какой же выбор сделать?", "Тени грешного города", "Повести о пространстве и времени", "Пьеса об Иване и Юлианне"]

    chaptCall = [[str(i) for i in range(-(len(config.chapters[0]) + 23), -5)]]

    items_chapt = []
    items = []
    callback = [str(i) for i in range(0, len(novels))]
    callback1 = [str(-i) for i in range(1, len(novels) + 1)]
    if call.data == 'full':
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(len(novels)):
            items.append(types.InlineKeyboardButton(text=novels[j], callback_data=callback[j]))
            markup_inline.add(items[j])
        bot.edit_message_text('Доступные произведения:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif(call.data == 'certain'):
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(len(novels)-3):
            items.append(types.InlineKeyboardButton(text=novels[j], callback_data=callback1[j]))
            markup_inline.add(items[j])
        bot.edit_message_text('Доступные произведения:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)
        #bot.edit_message_text('В разрабтке...', call.message.chat.id, call.message.message_id)
    elif(call.data == callback[0]):
        bot.edit_message_text('Отличный выбор!', call.message.chat.id, call.message.message_id)
        file = open("novels/Наше счастливое вчера.docx", "rb")
        
        bot.send_document(call.message.chat.id, file)
        
        ############
    elif (call.data == callback[1]):
        bot.edit_message_text('Классика!', call.message.chat.id, call.message.message_id)
        file = open("novels/роман.docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file.close()
    elif (call.data == callback[2]):
        bot.edit_message_text('Опять Алехины...', call.message.chat.id, call.message.message_id)
        file = open("novels/роман_2.docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file.close()
    elif (call.data == callback[3]):
        bot.edit_message_text('Немного мистики на улицах Петербурга? Почему бы и нет)', call.message.chat.id, call.message.message_id)
        file = open("Тени грешного города.docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file.close()
    elif (call.data == callback[4]):
        bot.edit_message_text('Длинная история о великих открытиях учеников 11 класса... Звучит интересно)', call.message.chat.id, call.message.message_id)
        file = open("novels/Повести о пространстве и времени.docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file.close()
    elif (call.data == callback[5]):
        bot.edit_message_text('Приготовьте чай! Самое время окунуться в атмосферу 19 века!', call.message.chat.id,
                              call.message.message_id)
        file = open("novels/Часть 1. Предательство лучшего друга..docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file = open("novels/Часть 2. Месть за прошлое..docx", "rb")
        bot.send_document(call.message.chat.id, file)
        file.close()

    elif (call.data == callback1[0]):
        #bot.edit_message_text('Отличный выбор!', call.message.chat.id, call.message.message_id)
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(6):
            if(j != 5):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[j])
            elif(j == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][42]))
                markup_inline.add(items_chapt[j])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][42]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 5
            if(i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][43]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][41]))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][43]):
            markup_inline = types.InlineKeyboardMarkup()
            items_chapt.clear()
            for i in range(7):
                j = i + 10
                if (i != 5 and i != 6):
                    items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                    markup_inline.add(items_chapt[i])
                elif (i == 5):
                    items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][44]))
                    markup_inline.add(items_chapt[i])
                else:
                    items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][40]))
                    markup_inline.add(items_chapt[i])

            bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][44]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 15
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][45]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][39]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][45]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 20
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][46]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][38]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][46]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 25
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][47]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][35]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][47]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 30
            if (i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][36]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][36]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 25
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][47]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][37]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][37]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 20
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][46]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][38]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id,reply_markup=markup_inline)

    elif (call.data == chaptCall[0][38]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 15
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][45]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][39]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][39]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 10
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][44]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][40]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == chaptCall[0][40]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 5
            if (i != 5 and i != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[i])
            elif (i == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][43]))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data=chaptCall[0][41]))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id,  reply_markup=markup_inline)

    elif (call.data == chaptCall[0][41]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(6):
            if (j != 5 and j != 6):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[0][j], callback_data=chaptCall[0][j]))
                markup_inline.add(items_chapt[j])
            elif (j == 5):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=chaptCall[0][42]))
                markup_inline.add(items_chapt[j])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == callback1[1]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(11):
            if(j != 10):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[j])
            elif(j == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=f'1next1'))
                markup_inline.add(items_chapt[j])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)
        #bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)

    elif(call.data == '1next1'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 10
            if (i != 10 and i != 11):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next2'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back1'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif(call.data == '1next2'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 20
            if (i != 10 and i != 11):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next3'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back2'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1next3'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 30
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next4'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back3'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1next4'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 40
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next5'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back4'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1next5'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(16):
            j = i + 50
            if (i != 15):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 15):
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back5'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1back5'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 40
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next5'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back4'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1back4'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 30
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next4'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back3'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1back3'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 20
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next3'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back2'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1back2'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 10
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next2'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='1back1'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '1back1'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(11):
            if (j != 10):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[1][j], callback_data=f'chpt1{str(j)}'))
                markup_inline.add(items_chapt[j])
            elif (j == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='1next1'))
                markup_inline.add(items_chapt[j])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)



    elif (call.data == callback1[2]):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for j in range(11):
            if(j != 10):
                items_chapt.append(types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[j])
            elif(j == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data=f'2next1'))
                markup_inline.add(items_chapt[j])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)


    elif (call.data == '2next1'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 10
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='2next2'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='2back1'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)


    elif (call.data == '2next2'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 20
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='2next3'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='2back2'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

    elif (call.data == '2next3'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(7):
            j = i + 30
            if (i != 6):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='2back3'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)



    elif (call.data == '2back3'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 20
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='2next3'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='2back2'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)


    elif (call.data == '2back2'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(12):
            j = i + 10
            if (i != 10 and i != 11):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][j], callback_data=f'chpt2{str(j)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='2next2'))
                markup_inline.add(items_chapt[i])
            else:
                items_chapt.append(types.InlineKeyboardButton(text="Назад", callback_data='2back1'))
                markup_inline.add(items_chapt[i])
        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)



    elif (call.data == '2back1'):
        items_chapt.clear()
        markup_inline = types.InlineKeyboardMarkup()
        for i in range(11):
            if (i != 10):
                items_chapt.append(
                    types.InlineKeyboardButton(text=config.chapters[2][i], callback_data=f'chpt2{str(i)}'))
                markup_inline.add(items_chapt[i])
            elif (i == 10):
                items_chapt.append(types.InlineKeyboardButton(text="Далее", callback_data='2next1'))
                markup_inline.add(items_chapt[i])

        bot.edit_message_text('Выберите главу:', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)






    elif (call.data == callback1[3]):
        bot.edit_message_text('Приношу свои извинения, но на данный момент роман находится в стадии написания и доступен только в полном виде...', call.message.chat.id, call.message.message_id)


    for g in range(36):
        if(call.data == chaptCall[0][g]):
            if(g != 35):
                filename = f"глава {g + 1}.docx"
                file = open(filename, "rb")
                bot.edit_message_text(f'Высылаю главу {g + 1}', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()
            else:
                filename = "Эпилог.docx"
                file = open(filename, "rb")
                bot.edit_message_text('Высылаю эпилог', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()
                #bot.edit_message_text(f'В разработке...', call.message.chat.id, call.message.message_id)


    for i in range(len(config.chapters[1])):
        if(call.data == f'chpt1{str(i)}'):
            if(i != len(config.chapters[1]) - 1):
                filename = f"novel1/глава {i + 1}.odt"
                file = open(filename, "rb")
                bot.edit_message_text(f'Высылаю главу {i + 1}', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()
            else:
                filename = "novel1/эпилог.odt"
                file = open(filename, "rb")
                bot.edit_message_text('Высылаю эпилог', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()

    for i in range(len(config.chapters[2])):
        if(call.data == f'chpt2{str(i)}'):
            if(i != len(config.chapters[2]) - 1):
                filename = f"novel2/глава {i + 1}.odt"
                file = open(filename, "rb")
                bot.edit_message_text(f'Высылаю главу {i + 1}', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()
            else:
                filename = "novel2/эпилог.odt"
                file = open(filename, "rb")
                bot.edit_message_text('Высылаю эпилог', call.message.chat.id, call.message.message_id)
                bot.send_document(call.message.chat.id, file)
                file.close()


    items_char = []

    for i in range(len(novels)):
        if (call.data == f"novel{str(i)}"):
            markup_inline = types.InlineKeyboardMarkup()
            if(i == 0):
                for j in range(len(config.characters[i])):
                    items_char.append(types.InlineKeyboardButton(text=config.characters[i][j], callback_data=f'chrt{str(i)}{str(j)}'))
                    markup_inline.add(items_char[j])
                bot.edit_message_text('А теперь двайте выберем персонажа', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)
            elif(i == 1):
                items_char.clear()
                for j in range(len(config.characters[i])):
                    items_char.append(types.InlineKeyboardButton(text=config.characters[i][j], callback_data=f'chrt{str(i)}{str(j)}'))
                    markup_inline.add(items_char[j])
                bot.edit_message_text('А теперь двайте выберем персонажа', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)
            elif (i == 2):
                items_char.clear()
                for j in range(len(config.characters[i])):
                    items_char.append(
                        types.InlineKeyboardButton(text=config.characters[i][j], callback_data=f'chrt{str(i)}{str(j)}'))
                    markup_inline.add(items_char[j])
                bot.edit_message_text('А теперь двайте выберем персонажа', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)

            elif (i == 3):
                items_char.clear()
                for j in range(len(config.characters[i])):
                    items_char.append(
                        types.InlineKeyboardButton(text=config.characters[i][j], callback_data=f'chrt{str(i)}{str(j)}'))
                    markup_inline.add(items_char[j])
                bot.edit_message_text('А теперь двайте выберем персонажа', call.message.chat.id, call.message.message_id, reply_markup=markup_inline)
            else:
                bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)

        elif(call.data == f"novel_{str(i)}"):
            bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)


    for i in range(len(config.characters[0])):
        if(call.data == f'chrt0{str(i)}'):
            bot.edit_message_text(config.inf_chrt[0][i], call.message.chat.id, call.message.message_id)


    for i in range(len(config.characters[1])):
        if(call.data == f'chrt1{str(i)}'):
            bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)


    for i in range(len(config.characters[2])):
        if(call.data == f'chrt2{str(i)}'):
            bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)

    for i in range(len(config.characters[3])):
        if(call.data == f'chrt3{str(i)}'):
            bot.edit_message_text('В разработке...', call.message.chat.id, call.message.message_id)

keep_alive()
bot.polling(none_stop=True, interval=0)