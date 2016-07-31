from event_lib import *

get_events_from_vk("pink floyd", "Москва")
artists = get_similar_artists("Сплин")
for artist in artists:
    print(artist)