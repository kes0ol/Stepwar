from sqlite3 import IntegrityError

from development.db.db import make_connection


# Вспомогательный класс для доступа к таблице user
class User:
    # Инициализация класса
    def __init__(self, id=None, nickname=None, created_at=None, updated_at=None):
        self.id = id  # Идентификатор записи
        self.nickname = nickname  # Nickname пользователя
        self.created_at = created_at  # Время создания записи
        self.updated_at = updated_at  # Время изменения записи

    # Отображение класса при печате
    def __repr__(self):
        return f"User {self.id} {self.nickname}"

    # Статический метод создания таблицы в базе данных
    @staticmethod
    def init_db():
        make_connection().cursor().execute(
            """CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(nickname)
            )""")

    # Статический метод для получения записей таблицы в виде списка экземпляров класса
    @staticmethod
    def get():
        records = []
        cursor = make_connection().cursor()
        cursor.execute("SELECT u.id, u.nickname, u.created_at, u.updated_at FROM user u ORDER BY u.id")
        for i in cursor.fetchall():
            records.append(User(*i))
        return records

    # Статический метод для получения записи таблицы с фильтрацией по start в виде списка экземплярa класса
    @staticmethod
    def get_by_nickname(nickname):
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT u.id, u.nickname, u.created_at, u.updated_at 
            FROM user u WHERE u.nickname LIKE ? ORDER BY u.id""",
            (nickname,))
        result = cursor.fetchall()
        if len(result):
            return User(*result[0])
        return None

    # Статический метод для получения записи таблицы по id в виде экземпляра класса
    @staticmethod
    def get_by_id(id):
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT u.id, u.nickname, u.created_at, u.updated_at 
            FROM user u WHERE u.id = ? ORDER BY u.id""",
            (id,))
        result = cursor.fetchall()
        if len(result):
            return User(*result[0])
        return None

    # Статический метод для добавления экземпляра класса в таблицу или изменения, если такая запись уже существует
    @staticmethod
    def add(user):
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

    # Статический метод для удаления экземпляра класса из таблицы
    @staticmethod
    def remove(user):
        connection = make_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id = ?", (user.id,))
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()


# Создать таблицу в момент импорта
User.init_db()
