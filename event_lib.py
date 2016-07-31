###### Класс для получения информации о событиях, связанных с заданным исполнителем, в заданном городе

import vk
import requests
from bs4 import BeautifulSoup

# авторизация в vk
session = vk.AuthSession(app_id='5299950', user_login='89889800727', user_password='VkRentProject420')

#session = vk.AuthSession(app_id='5299950', user_login='89889800727', user_password='VkRentProject420')
api = vk.API(session)

# получаем список городов России
cities = api.database.getCities(country_id = 1)


def get_events_from_vk(artist_name, event_city):
    current_city_id = 1
    for city in cities:
        if isinstance(city, dict):
            if city["title"] == event_city:
                current_city_id = city["cid"]
                break
    events = api.groups.search(q = artist_name, type = "event", country_id = 1, city_id = current_city_id, future = 1)
    if len(events) > 0:
        events = events[1:]
    #for event in events:
    #    if isinstance(event, dict):
    #       print(event["name"])
    return events


# Возвращает список похожих исполнителей, используя API Muzis
def get_similar_artists(artist_name):
    try:
        r = requests.post("http://muzis.ru/api/search.api", data={'q_performer': artist_name})
        data = r.json()
        if len(data["performers"]) == 1:
            performer_id = data["performers"][0]
            performer_id = performer_id["id"]
            r = requests.post("http://muzis.ru/api/similar_performers.api", data={'performer_id': performer_id})
            data = r.json()
            for performer in data["performers"]:
                yield performer["title"]
        return -1
    except BaseException as e:
        print(str(e))
        return -1


def get_artist_song(artist_name):
    songs = api.audio.search(q = artist_name, oauth = "RjEWmZ4dWmjQrlrLwa7G")
    if len(songs) > 0:
        return songs[0]["url"]



