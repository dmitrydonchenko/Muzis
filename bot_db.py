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


# Класс таблицы пользователей и событий в БД
class Users_Events(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users')
    event_id = peewee.ForeignKeyField(Events, db_column='event_id', to_field='id', related_name='events')


