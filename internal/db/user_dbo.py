from sqlite3 import IntegrityError

from internal.db.db import make_connection


class User:
    '''Вспомогательный класс для доступа к таблице user'''

    def __init__(self, id=None, nickname=None, created_at=None, updated_at=None):
        '''Инициализация класса'''
        self.id = id  # Идентификатор записи
        self.nickname = nickname  # Nickname пользователя
        self.created_at = created_at  # Время создания записи
        self.updated_at = updated_at  # Время изменения записи

    def __repr__(self):
        '''Отображение класса при печате'''
        return f"User {self.id} {self.nickname}"

    @staticmethod
    def init_db():
        '''Статический метод создания таблицы в базе данных'''
        make_connection().cursor().execute(
            """CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(nickname)
            )""")

    @staticmethod
    def get():
        '''Статический метод для получения записей таблицы в виде списка экземпляров класса'''
        records = []
        cursor = make_connection().cursor()
        cursor.execute("SELECT u.id, u.nickname, u.created_at, u.updated_at FROM user u ORDER BY u.id")
        for i in cursor.fetchall():
            records.append(User(*i))
        return records

    @staticmethod
    def get_by_nickname(nickname):
        '''Статический метод для получения записи таблицы с фильтрацией по start в виде списка экземплярa класса'''
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT u.id, u.nickname, u.created_at, u.updated_at 
            FROM user u WHERE u.nickname LIKE ? ORDER BY u.id""",
            (nickname,))
        result = cursor.fetchall()
        if len(result):
            return User(*result[0])
        return None

    @staticmethod
    def get_by_id(id):
        '''Статический метод для получения записи таблицы по id в виде экземпляра класса'''
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT u.id, u.nickname, u.created_at, u.updated_at 
            FROM user u WHERE u.id = ? ORDER BY u.id""",
            (id,))
        result = cursor.fetchall()
        if len(result):
            return User(*result[0])
        return None

    @staticmethod
    def add(user):
        '''Статический метод для добавления экземпляра класса в таблицу или изменения, если такая запись уже существует'''
        connection = make_connection()
        cursor = connection.cursor()
        try:
            if user.id is None:
                cursor.execute(
                    """INSERT INTO user (nickname) VALUES (?) 
                    RETURNING id, created_at, updated_at""",
                    (user.nickname,))
                user.id, user.created_at, user.updated_at = cursor.fetchone()
            else:
                cursor.execute(
                    """UPDATE score SET nickname = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?""""",
                    (user.nickname, user.id))
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()

    @staticmethod
    def remove(user):
        '''Статический метод для удаления экземпляра класса из таблицы'''
        connection = make_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id = ?", (user.id,))
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()


# Создание таблицы в момент импорта
User.init_db()
