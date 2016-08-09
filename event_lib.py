###### Класс для получения информации о событиях, связанных с заданным исполнителем, в заданном городе

import vk
import requests

# авторизация в vk
session = vk.AuthSession(app_id='5299950', user_login='89889800727', user_password='')
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
    events = api.groups.search(q = artist_name, type = "event", count = 10, country_id = 1, city_id = current_city_id, future = 1)
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
    try:
        r = requests.post("http://muzis.ru/api/search.api", data={'q_performer': artist_name})
        data = r.json()
        if len(data["performers"]) == 1:
            performer_id = data["performers"][0]
            performer_id = performer_id["id"]
            r = requests.post("http://muzis.ru/api/get_songs_by_performer.api", data={'performer_id': performer_id})
            data = r.json()
            songs = data["songs"]
            if len(songs) > 0:
                filename = songs[0]["file_mp3"]
                r = requests.get("http://f.muzis.ru/" + filename)
                data = r.json()
        return -1
    except BaseException as e:
        print(str(e))
        return -1



