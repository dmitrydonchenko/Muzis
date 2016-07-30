import config
import telebot
import event_lib
import bot_db
from enum import Enum

class BotStates(Enum):
    Waiting = 0
    AddingArtists = 1
    GettingEvents = 2
    GettingArtisEvents = 3
    FindingSoulmates = 4

bot = telebot.TeleBot(config.token)

bot_state = BotStates.Waiting

user_location = ""

help_string = []
help_string.append('/start - начать общение с ботом;\n')
help_string.append('/help - вывод справки;\n')
help_string.append('/addArtists - добавить новых исполнителей;\n')
help_string.append('/checkinEvent - зачекиниться на события;\n')
help_string.append('/getArtistEvents - вывод событий по исполнителю;\n')
help_string.append('/findSoulmates - найти людей, которые идут на то же событие.\n')

@bot.message_handler(commands=["start", "help"])
def greetings(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, соединяющий души.\n')
    bot.send_message(message.chat.id, 'Напиши пожалуйста, где ты находишься')

@bot.message_handler(commands=["addArtists"])
def add_artists(message):
    global bot_state
    bot.send_message(message.chat.id, 'Напиши мне через запятую список своих любимых исполнителей')
    bot_state = BotStates.AddingArtists

@bot.message_handler(content_types=["text"])
def handle_dialog(message):
    global bot_state
    global user_location
    if (bot_state == BotStates.Waiting):
        user_location = message.text
        bot.send_message(message.chat.id, 'Благодарю! Давай поищем, чем ты сможешь здесь заняться.')
        bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")
    if (bot_state == BotStates.AddingArtists):
        artists = parse_artists(message.text)

        for artist in artists:
            db_save_artist(artist)


        bot.send_message(message.chat.id, 'Я запомнил следующих твоих любимых исполнителей:\n\n' + "".join(artists))

def parse_artists(artists_string):
    return [x.strip() + '\n' for x in artists_string.split(',')]

def db_save_artist(artist):
    events = event_lib.get_events_from_vk(artist, user_location)
    for event in events:
        url = 'vk.com/' + event.screen_name
        if not bot_db.is_event_exist(url):
            bot_db.insert_event(event.name, url, user_location)

if __name__ == '__main__':
     bot.polling(none_stop=True)