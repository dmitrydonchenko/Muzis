import config
import telebot
import event_lib
import bot_db
import shelve

from enum import Enum

def write_to_file(filename, data):
    file = open(filename, 'a+')
    file.write(data)
    file.close()

class BotStates(Enum):
    Waiting = 0
    AddingArtists = 1
    SetLocation = 2
    CheckinEvents = 3
    GettingArtisEvents = 4
    FindingSoulmates = 5

bot = telebot.TeleBot(config.token)

help_string = []
help_string.append('/start - начать общение с ботом;\n')
help_string.append('/help - вывод справки;\n')
help_string.append('/addArtists - добавить новых исполнителей;\n')
help_string.append('/setLocation - добавить новых исполнителей;\n')
help_string.append('/getPossibleEvents - куда пойти;\n')
help_string.append('/checkinEvents - зачекиниться на события;\n')
help_string.append('/getArtistEvents - вывод событий по исполнителю;\n')
help_string.append('/findSoulmates - найти людей, которые идут на то же событие;\n')
help_string.append('/getSimilarArtists - найти исполнителей, которые могут тебе понравиться.\n')

@bot.message_handler(commands=["start"])
def greetings(message):
    try:
        first_name = ""
        last_name = ""
        login = ""
        if (message.from_user.first_name != None):
            first_name = message.from_user.first_name
        if (message.from_user.last_name != None):
            last_name = message.from_user.last_name
        if (message.from_user.username != None):
            login = message.from_user.username

        bot_db.insert_user(str(message.from_user.id), first_name + ' ' + last_name, login)
        bot.send_message(message.chat.id, 'Привет! Я бот, соединяющий души.')
        greetings(message)
        if get_location(message.chat.id) == None:
            bot.send_message(message.chat.id, 'Я пока не знаю, в каком ты городе.')
            set_user_location(message)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["getSimilarArtists"])
def get_similar_artists(message):
    try:
        artists = bot_db.get_favourite_artists(str(message.chat.id))
        for artist in artists:
            for similar_artist in event_lib.get_similar_artists(artist.artist_id.id):
                bot.send_message(message.chat.id, similar_artist)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["help"])
def greetings(message):
    try:
        bot.send_message(message.chat.id, ''.join(help_string))
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["addArtists"])
def add_artists(message):
    try:
        bot.send_message(message.chat.id, 'Напиши мне через запятую список своих любимых исполнителей')
        # with shelve.open(config.bot_state_db) as db:
        #     db[message.chat.id] = BotStates.AddingArtists
        set_bot_state(message.chat.id, BotStates.AddingArtists)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["findSoulmates"])
def find_soulmates(message):
    try:
        bot.send_message(message.chat.id, 'У следующих пользователей схожие с тобой музыкальные вкусы и ты с ними можешь пересечься на интересных вам обоим событиях. Не стесняйся знакомиться с ними. Музыка объединяет!')
        events = bot_db.get_user_events(message.chat.id)
        for event in events:
            soulmates = bot_db.get_soulmates(str(message.chat.id), event.id)
            for soulmate in soulmates:
                if soulmate.login != None:
                    bot.send_message(message.chat.id, '@' + soulmate.login)
    except BaseException as e:
        write_to_file("errors.txt", str(e))
    # with shelve.open(config.bot_state_db) as db:
    #     db[message.chat.id] = BotStates.AddingArtists

@bot.message_handler(commands=["setLocation"])
def set_user_location(message):
    try:
        bot.send_message(message.chat.id, 'Напиши мне, где ты находишься')
        # with shelve.open(config.bot_state_db) as db:71
        #     db[message.chat.id] = BotStates.SetLocation
        set_bot_state(message.chat.id, BotStates.SetLocation)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        if call.message:
            bot_db.checkin_user(call.message.chat.id, int(call.data))
            bot.send_message(call.message.chat.id, 'Поздравляю! Ты идёшь на выбранное событие')
            bot.send_message(call.message.chat.id, 'Хочешь узнать, кто ещё пойдёт на это событие? Воспользуйся командой /findSoulmates', parse_mode='Markdown')
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["checkinEvents"])
def checkin_events(message):
    try:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for event in bot_db.get_user_possible_events(message.chat.id):
            if event.city == get_location(message.chat.id):
                callback_button = telebot.types.InlineKeyboardButton(text=event.event_name, callback_data=str(event.id))
                keyboard.add(callback_button)
        bot.send_message(message.chat.id, 'На какое из следующих событий ты хочешь пойти?', reply_markup = keyboard)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(commands=["getPossibleEvents"])
def get_possible_events(message):
    try:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for event in bot_db.get_user_possible_events(str(message.chat.id)):
            if event.city == get_location(message.chat.id):
                callback_button = telebot.types.InlineKeyboardButton(text=event.event_name, url=event.url)
                keyboard.add(callback_button)

        bot.send_message(message.chat.id, 'Нажми на событие, чтобы узнать о нём поподробнее', reply_markup = keyboard)
        bot.send_message(message.chat.id, 'Чтобы зачекинится на событие воспользуйся командой /checkinEvents', parse_mode='Markdown')
        bot.send_message(message.chat.id, 'Если события не отобразились, то воспользуйся командой /addArtists для добавления исполнителей', parse_mode='Markdown')
    except BaseException as e:
        write_to_file("errors.txt", str(e))

@bot.message_handler(content_types=["text"])
def handle_dialog(message):
    try:
        bot_state = get_state(message.chat.id)
        # with shelve.open(config.bot_state_db) as db:
        #     bot_state = db[message.chat.id][bot_state]
        if (bot_state == BotStates.AddingArtists):
            artists = parse_artists(message.text)

            for artist in artists:
                db_save_artist(message.chat.id, artist)

            bot.send_message(message.chat.id, 'Я запомнил следующих твоих любимых исполнителей:\n\n' + "\n".join(artists))
            bot.send_message(message.chat.id, 'Если хочешь послушать музыку, которая похожа на твои музыкальные функции, то воспользуйся функцией /getSimilarArtists',
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, 'Чтобы посмотреть список интересных событий, связанных с твоими любимыми исполнителями, воспользуйся командой /getPossibleEvents',
                             parse_mode='Markdown')
        elif (bot_state == BotStates.SetLocation):
            # with shelve.open(config.location_db) as db:
            #     db[message.chat.id] = message.text
            set_location(message.chat.id, message.text)
            artists = bot_db.get_favourite_artists(message.chat.id)
            for artist in artists:
                events = event_lib.get_events_from_vk(artist.artist_id.id, message.text)
                for event in events:
                    url = 'vk.com/' + event['screen_name']
                    bot_db.insert_event(event['name'], url, message.text, artist.artist_id.id)
            bot.send_message(message.chat.id, 'Ты всегда можешь изменить свой город командой /setLocation', parse_mode="Markdown")
            bot.send_message(message.chat.id, 'А посмотреть список музыкальных событий в городе можно командой /getPossibleEvents',
                             parse_mode="Markdown")
        set_bot_state(message.chat.id, BotStates.Waiting)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def parse_artists(artists_string):
    try:
        res = [x.strip().lower() for x in artists_string.split(',')]
        return res
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def db_save_artist(user_id, artist):
    try:
        bot_db.insert_artist(artist)
        bot_db.insert_user_artist(str(user_id), artist)
        location = get_location(user_id)
        events = event_lib.get_events_from_vk(artist, location)
        for event in events:
            url = 'vk.com/' + event['screen_name']
            bot_db.insert_event(event['name'], url, location, artist)
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def set_bot_state(user_id, bot_state):
    try:
        with shelve.open(config.bot_state_db) as db:
            db[str(user_id)] = bot_state
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def get_state(user_id):
    try:
        bot_state = BotStates.Waiting
        with shelve.open(config.bot_state_db) as db:
            if str(user_id) in db.keys():
                bot_state = db[str(user_id)]
        return bot_state
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def set_location(user_id, location):
    try:
        with shelve.open(config.location_db) as db:
            db[str(user_id)] = location
    except BaseException as e:
        write_to_file("errors.txt", str(e))

def get_location(user_id):
    try:
        location = None
        with shelve.open(config.location_db) as db:
            if str(user_id) in db.keys():
                location = db[str(user_id)]
        return location
    except BaseException as e:
        write_to_file("errors.txt", str(e))

if __name__ == '__main__':
     bot.polling(none_stop=True)