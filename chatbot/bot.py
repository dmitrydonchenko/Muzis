import config
import telebot
from enum import Enum

class BotStates(Enum):
    Waiting = 0
    AddingArtists = 1
    GettingEvents = 2
    GettingArtisEvents = 3
    FindingSoulmates = 4

bot = telebot.TeleBot(config.token)

bot_state = BotStates.Waiting

help_string = []
help_string.append('Привет! Я бот, соединяющий души\n\n')
help_string.append('/start - начать общение с ботом;\n')
help_string.append('/help - вывод справки;\n')
help_string.append('/addArtists - добавить новых исполнителей;\n')
help_string.append('/getEvent - зачекиниться на события;\n')
help_string.append('/getArtistEvents - вывод событий по исполнителю;\n')
help_string.append('/findSoulmates - найти людей, которые идут на то же событие.\n')

@bot.message_handler(commands=["start", "help"])
def greetings(message):
    bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")

@bot.message_handler(commands=["addArtists"])
def add_artists(message):
    global bot_state
    bot.send_message(message.chat.id, "Напиши мне через запятую список своих любимых исполнителей")
    bot_state = BotStates.AddingArtists

@bot.message_handler(content_types=["text"])
def handle_dialog(message):
    global bot_state
    if (bot_state == BotStates.AddingArtists):
        bot.send_message(message.chat.id, 'Я запомнил следующих твоих любимых исполнителей:\n\n' + "".join(parse_artists(message.text)))

def parse_artists(artists_string):
    return [x.strip() + '\n' for x in artists_string.split(',')]

if __name__ == '__main__':
     bot.polling(none_stop=True)