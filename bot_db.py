####### Класс работы с БД пользователей и событий ########

import peewee

db = peewee.MySQLDatabase('muzis', user='vkrent', passwd='VkRentDb')


class MySQLModel(peewee.Model):
    class Meta:
        database = db


# Класс таблицы пользователей в БД
class Users(MySQLModel):
    id = peewee.CharField(primary_key=True)   # id пользователя в мессенджере
    user_name = peewee.CharField()            # имя пользователя


# Класс таблицы событий в БД
class Events(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    event_name = peewee.CharField()
    url = peewee.CharField()
    city = peewee.CharField()
    artist_id = peewee.ForeignKeyField(Artists, db_column='artist_id', to_field='id', related_name='artists_events')


# Класс таблицы исполнителей
class Artists(MySQLModel):
    id = peewee.CharField(primary_key=True)


# Класс таблицы исполнителей и пользователей
class UsersArtists(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users_artists')
    artist_id = peewee.ForeignKeyField(Events, db_column='artist_id', to_field='id', related_name='artists_users')


# Класс таблицы пользователей и событий в БД
class UsersEvents(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users_events')
    event_id = peewee.ForeignKeyField(Events, db_column='event_id', to_field='id', related_name='events_users')

############# Методы добавления ################


# Добавляет нового пользователя в БД
def insert_user(user_id, name):
    if not is_user_exists(user_id):
        res = Users.insert(id = user_id, user_name = name).execute()
        return res
    return -1


# Добавляет новое событие в БД
def insert_event(name, event_url, event_city, artist_name):
    if not is_event_exists(event_url):
        res = Events.insert(event_name = name, url = event_url, city = event_city, artist_id = artist_name).execute()
        return res
    return -1


# Добавляет нового участника события
def insert_user_event(m_user_id, m_event_id):
    res = UsersEvents.insert(user_id = m_user_id, event_id = m_event_id).execute()


# Добавить пользователя в список участников события
def checkin_user(m_user_id, m_event_id):
    res = UsersEvents.insert(user_id = m_user_id, event_id = m_event_id).execute()
    return res


# Добавить исполнителя
def insert_artist(artist_name):
    if not is_artist_exists(artist_name):
        res = Artists.insert(id = artist_name).execute()
        return res
    return -1


# Добавить исполнителя в список любимых у пользователя
def insert_user_artist(m_user_id, m_artist_name):
    res = UsersArtists.insert(user_id = m_user_id, artist_id = m_artist_name).execute()
    return res

######## Методы для получения данных из БД ############


# Возвращает список событий любимых исполнителей пользователя
def get_user_possible_events(user_id):
    db.connect()
    users_favourite_artists = UsersArtists.select(UsersArtists.artist_id).where(UsersArtists.user_id == user_id)
    for artist in users_favourite_artists:
        yield Events.select().where(Events.artist_id == artist.id)
    db.close()


# Возвращает список событий, на которые идет пользователь
def get_user_events(user_id):
    db.connect()
    user_events = Events.select(Users, Events, ).join(UsersEvents.user_id == user_id and Events.id == UsersEvents.id)
    db.close()
    return user_events.get()


# Возвращает список участников события
def get_users_by_event(event_id):
    db.connect()
    users = Users.select().join(UsersEvents.event_id == event_id, UsersEvents.user_id == Users.id)
    db.close()
    return users


########## Методы проверки ################


# Возвращает True, если исполнитель с таким именем уже существует
def is_artist_exists(artist_name):
    db.connect()
    if (Artists.select().where(Artists.id == artist_name)).count() > 0:
        db.close()
        return True
    db.close()
    return False


# Возвращает True, если событие с данным url уже есть в БД
def is_event_exists(event_url):
    db.connect()
    if (Events.select().where(Events.url == event_url)).count() > 0:
        db.close()
        return True
    db.close()
    return False


# Возвращает True, если пользователь с таким id уже существует
def is_user_exists(user_id):
    db.connect()
    if (Users.select().where(Users.id == user_id)).count() > 0:
        db.close()
        return True
    db.close()
    return False


