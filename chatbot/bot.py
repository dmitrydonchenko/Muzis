import config
import telebot
import event_lib
import bot_db
import shelve

from enum import Enum

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
help_string.append('/findSoulmates - найти людей, которые идут на то же событие.\n')

@bot.message_handler(commands=["start"])
def greetings(message):
    bot_db.insert_user(str(message.from_user.id), message.from_user.first_name + ' ' + message.from_user.last_name)
    bot.send_message(message.chat.id, 'Привет! Я бот, соединяющий души.')
    if get_location(message.chat.id) == None:
        bot.send_message(message.chat.id, 'Я пока не знаю, в каком ты городе.')
        set_user_location(message)

@bot.message_handler(commands=["help"])
def greetings(message):
    bot.send_message(message.chat.id, ''.join(help_string))

@bot.message_handler(commands=["addArtists"])
def add_artists(message):
    bot.send_message(message.chat.id, 'Напиши мне через запятую список своих любимых исполнителей')
    # with shelve.open(config.bot_state_db) as db:
    #     db[message.chat.id] = BotStates.AddingArtists
    set_bot_state(message.chat.id, BotStates.AddingArtists)

@bot.message_handler(commands=["setLocation"])
def set_user_location(message):
    bot.send_message(message.chat.id, 'Напиши мне, где ты находишься')
    # with shelve.open(config.bot_state_db) as db:
    #     db[message.chat.id] = BotStates.SetLocation
    set_bot_state(message.chat.id, BotStates.SetLocation)

@bot.message_handler(commands=["checkinEvents"])
def checkin_events(message):
    bot.send_message(message.chat.id, 'Напиши через запятую, на какие из следующих событий ты хочешь пойти:')

    events = bot_db.get_user_possible_events(message.chat.id)
    for event in events:
        bot.send_message(message.chat.id, event.url)

    with shelve.open(config.bot_state_db) as db:
        db[message.chat.id] = BotStates.CheckinEvents

@bot.message_handler(commands=["getPossibleEvents"])
def get_possible_events(message):
    for event in bot_db.get_user_possible_events(str(message.chat.id)):
        if event != None:
            bot.send_message(message.chat.id, event.url)


@bot.message_handler(content_types=["text"])
def handle_dialog(message):
    bot_state = get_state(message.chat.id)
    # with shelve.open(config.bot_state_db) as db:
    #     bot_state = db[message.chat.id][bot_state]
    if (bot_state == BotStates.AddingArtists):
        artists = parse_artists(message.text)

        for artist in artists:
            db_save_artist(message.chat.id, artist)

        bot.send_message(message.chat.id, 'Я запомнил следующих твоих любимых исполнителей:\n\n' + "\n".join(artists))
    elif (bot_state == BotStates.SetLocation):
        # with shelve.open(config.location_db) as db:
        #     db[message.chat.id] = message.text
        set_location(message.chat.id, message.text)
        bot.send_message(message.chat.id, 'Я запомню :)')
        bot.send_message(message.chat.id, 'Ты всегда можешь изменить свой город командой /setLocation', parse_mode="Markdown")

    set_bot_state(message.chat.id, BotStates.Waiting)

def parse_artists(artists_string):
    return [x.strip().lower() for x in artists_string.split(',')]

def db_save_artist(user_id, artist):
    bot_db.insert_artist(artist)
    bot_db.insert_user_artist(str(user_id), artist)
    location = get_location(user_id)
    events = event_lib.get_events_from_vk(artist, location)
    for event in events:
        url = 'vk.com/' + event['screen_name']
        bot_db.insert_event(event['name'], url, location, artist)

def set_bot_state(user_id, bot_state):
    with shelve.open(config.bot_state_db) as db:
        db[str(user_id)] = bot_state

def get_state(user_id):
    bot_state = BotStates.Waiting
    with shelve.open(config.bot_state_db) as db:
        if str(user_id) in db.keys():
            bot_state = db[str(user_id)]
    return bot_state

def set_location(user_id, location):
    with shelve.open(config.location_db) as db:
        db[str(user_id)] = location

def get_location(user_id):
    location = None
    with shelve.open(config.location_db) as db:
        if str(user_id) in db.keys():
            location = db[str(user_id)]
    return location

if __name__ == '__main__':
     bot.polling(none_stop=True)