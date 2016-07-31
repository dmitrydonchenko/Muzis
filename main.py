from event_lib import *
import vlc

events = get_events_from_vk("Pink Floyd", "Москва")
for event in events:
    print (event["name"])
artists = get_similar_artists("Pink Floyd")
for artist in artists:
    print(artist)
url = get_artist_song("Pink Floyd")
print(url)