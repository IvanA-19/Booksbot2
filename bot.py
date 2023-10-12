from telebot import TeleBot, types
from config import *

bot = TeleBot(api_token)


def get_reply_keyboard(keyboard_buttons: list,
                       one_time: bool = False,
                       menu_keyboard: bool = False) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=one_time)

    def get_menu_keyboard() -> None:
        for i in range(len(keyboard_buttons)):
            if i == 1:
                keyboard.add(types.KeyboardButton(text=keyboard_buttons[i]),
                             types.KeyboardButton(text=keyboard_buttons[i + 1]))
            elif i == 2:
                continue
            else:
                keyboard.add(types.KeyboardButton(text=keyboard_buttons[i]))

    if not menu_keyboard:
        for button in keyboard_buttons:
            keyboard.add(types.KeyboardButton(button))
    else:
        get_menu_keyboard()

    return keyboard


def get_inline_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for i, novel in enumerate(novels):
        keyboard.add(types.InlineKeyboardButton(text=novel, callback_data=novels_callback_id[i]))
    return keyboard


def get_inline_keyboard_for_novel(novel: str) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Описание', callback_data=f'about {novels.index(novel)}'),
                 types.InlineKeyboardButton(text='Персонажи', callback_data=f'characters {novels.index(novel)}'))
    keyboard.add(types.InlineKeyboardButton(text='Меню', callback_data='menu'))
    return keyboard


def get_user(message) -> str:
    user = message.from_user.first_name
    if message.from_user.last_name is not None:
        user += f' {message.from_user.last_name}'
    return user


@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message)
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    bot.send_message(message.chat.id, f'Рад приветствовать, {user}!\n'
                                      'Для отображения списка команд используй /help'
                                      '\nДля получения информации используй /info\n'
                                      'Чтобы открыть список контактов используй /contacts', reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def menu(message):
    menu_keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
    bot.send_message(message.chat.id, 'Меню открыто \U00002705', reply_markup=menu_keyboard)


@bot.message_handler(commands=['help'])
def help_list(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    bot.send_message(message.chat.id, text=helpList, reply_markup=keyboard)


@bot.message_handler(commands=['contacts'])
def contacts_list(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    bot.send_message(message.chat.id, text=contacts, reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def information(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    bot.send_message(message.chat.id, text=info, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Завершить работу \U0001F4A4':
        keyboard = get_reply_keyboard(keyboard_buttons=['СТАРТ'], one_time=True)
        bot.send_message(message.chat.id,
                         'Было приятно с вами работать!\nВсего доброго\U0001FAE1',
                         reply_markup=keyboard)
    elif message.text == 'Меню':
        keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
        bot.send_message(message.chat.id, 'Выберите, что вы хотите сделать\U0001F607', reply_markup=keyboard)

    elif message.text == 'Выбрать произведение \U0001F4DA':
        keyboard = get_inline_keyboard()
        bot.send_message(message.chat.id, 'Какое произведение вас интересует?', reply_markup=keyboard)

    elif message.text == 'СТАРТ':
        user = get_user(message)
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        bot.send_message(message.chat.id, f'Приветсвую, {user}!\nДля открытия меню жми кнопку',
                         reply_markup=keyboard)
    elif message.text == 'Контакты \U0001F4D3':
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        bot.send_message(message.chat.id, text=contacts, reply_markup=keyboard)
    elif message.text == 'Информация \U00002139':
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        bot.send_message(message.chat.id, text=info, reply_markup=keyboard)
    else:
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        bot.send_message(message.chat.id, 'Прости, я не понимаю \U0001F97A\n'
                                          'Исполбзуй /help для просмотра списка команд \U0001F9D0\n'
                                          'Или жми на кнопку Меню \U0001F92F', reply_markup=keyboard)


@bot.message_handler(content_types=['new_chat_members'])
def hello_member(message):
    user = get_user(message)
    bot.send_message(message.chat.id, text=f'Приветствую, {user}!{hello}')


@bot.callback_query_handler(func=lambda call: True)
def process_callback(call):
    def check_callback() -> None:
        for i, element in enumerate(novels_callback_id):
            if call.data == element:
                file = open(f'data/novels/{novels[i]}.docx', 'rb')
                keyboard = get_inline_keyboard_for_novel(novels[i])
                bot.edit_message_text('Приятного прочтения\U0001F60A', call.message.chat.id, call.message.id)
                bot.send_document(call.message.chat.id, document=file, reply_markup=keyboard)

        for i, element in enumerate(characters_callback_id):
            if call.data == element:
                if 'characters' in element:
                    # Delete if when all files with characters be in folder
                    if i > 0:
                        bot.send_message(call.message.chat.id, 'В разработке...')
                        print(i)
                    else:
                        file = open(f'data/characters/{novels[i]} персонажи.docx', 'rb')
                        bot.send_message(call.message.chat.id, 'Все песонажи в файле\U0001F60F')
                        bot.send_document(call.message.chat.id, document=file)
        for i, element in enumerate(about_callback_id):
            # Delete if when description will be in folder about
            if call.data == element:
                if not(i >= 0):
                    file = open(f'data/about/{novels[i]} о романе.docx', 'rb')
                    bot.send_message(call.message.chat.id, 'Описание романа в файле\U0001F60C')
                    bot.send_document(call.message.chat.id, document=file)
                else:
                    bot.send_message(call.message.chat.id, 'В разработке...')

        if call.data == 'menu':
            keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
            bot.send_message(call.message.chat.id, 'Выберите, что вы хотите сделать\U0001F607',
                             reply_markup=keyboard)

    check_callback()
