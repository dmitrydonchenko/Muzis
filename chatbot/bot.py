import config
import telebot
from enum import Enum

class BotStates(Enum):
    AddingArtists = 0
    GettingEvents = 1
    GettingArtisEvents = 2
    FindingSoulmates = 3

bot = telebot.TeleBot(config.token)

greetings_str = 'Привет! Я бот, соединяющий души\n\n'

help_string = []
help_string.append(greetings_str)
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
    bot.send_message(message.chat.id, "Напиши мне через запятую список своих любимых исполнителей")

@bot.message_handler(content_types="text")
def adding_artist(chat_id):
    bot.send_message(message.chat.id, "Напиши мне через запятую список своих любимых исполнителей")

if __name__ == '__main__':
     bot.polling(none_stop=True)