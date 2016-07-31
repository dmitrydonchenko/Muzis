from event_lib import *
import vlc

events = get_events_from_vk("pink floyd", "Москва")
artists = get_similar_artists("Pink Floyd")
for artist in artists:
    print(artist)
url = get_artist_song("Pink Floyd")
print(url)