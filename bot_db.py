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


# Класс таблицы пользователей и событий в БД
class UsersEvents(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users')
    event_id = peewee.ForeignKeyField(Events, db_column='event_id', to_field='id', related_name='events')


# Добавляет нового пользователя в БД
def insert_user(user_id, name):
    res = Users.insert(id = user_id, user_name = name).execute()
    return res


# Добавляет новое событие в БД
def insert_event(name, event_url, event_city):
    res = Events.insert(event_name = name, url = event_url, city = event_city).execute()
    return res


# Добавляет нового участника события
def insert_user_event(m_user_id, m_event_id):
    res = UsersEvents.insert(user_id = m_user_id, event_id = m_event_id).execute()


# Возвращает True, если событие с данным url уже есть в БД
def is_event_exist(event_url):
    db.connect()
    if (Events.select().where(Events.url == event_url)).count() > 0:
        db.close()
        return True
    db.close()
    return False


# Возвращает список событий, на которые идет пользователь
def get_user_events(user_id):
    db.connect()
    user_events = Events.select().join(UsersEvents.user_id == user_id, Events.id == UsersEvents.id)
    db.close()
    return user_events


# Возвращает список участников события
def get_events_by_user(event_id):
    db.connect()
    users = Users.select().join(UsersEvents.event_id == event_id, UsersEvents.user_id == Users.id)
    db.close()
    return users


# Добавить пользователя в список участников события
def checkin_user(m_user_id, m_event_id):
    res = UsersEvents.insert(user_id = m_user_id, mevent_id = m_event_id).execute()


