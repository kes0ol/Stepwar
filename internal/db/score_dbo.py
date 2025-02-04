from sqlite3 import IntegrityError

from internal.db.db import make_connection


# Вспомогательный класс для доступа к таблице score
class Score:
    # Инициализация класса
    def __init__(self, id=None, user_id=None, level=None, score_points=None, created_at=None, updated_at=None):
        self.id = id  # Идентификатор записи
        self.user_id = user_id  # Идентификатор записи в таблице users
        self.level = level  # Номер уровня
        self.score_points = score_points  # Количество набранных очков
        self.created_at = created_at  # Время создания записи
        self.updated_at = updated_at  # Время изменения записи

    # Отображение класса при печате
    def __repr__(self):
        return f"Score {self.id} {self.user_id} {self.level} {self.score_points} {self.created_at} {self.updated_at}"

    # Статический метод создания таблицы в базе данных
    @staticmethod
    def init_db():
        make_connection().cursor().execute(
            """CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level INTEGER NOT_NULL,
            score_points INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
            )""")

    # Статический метод для получения записей таблицы в виде списка экземпляров класса
    @staticmethod
    def get():
        records = []
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT s.id, s.user_id, s.level, s.score_points, s.created_at, s.updated_at 
            FROM score s ORDER BY s.id
            """)
        for i in cursor.fetchall():
            records.append(Score(*i))
        return records

    # Статический метод для получения записи таблицы по id в виде экземпляра класса
    @staticmethod
    def get_by_id(id):
        cursor = make_connection().cursor()
        cursor.execute(
            """SELECT s.id, s.user_id, s.level, s.score_points, s.created_at, s.updated_at 
            FROM score s WHERE s.id = ? ORDER BY s.id""",
            (id,))
        result = cursor.fetchall()
        if len(result):
            return Score(*result[0])
        return None

    # Статический метод для добавления экземпляра класса в таблицу или изменения, если такая запись уже существует
    @staticmethod
    def add(score):
        connection = make_connection()
        cursor = connection.cursor()
        try:
            if score.id is None:
                cursor.execute(
                    """INSERT INTO score (user_id, level, score_points) VALUES (?, ?, ?) 
                    RETURNING id, created_at, updated_at""",
                    (score.user_id, score.level, score.score_points))
                score.id, score.created_at, score.updated_at = cursor.fetchone()
            else:
                cursor.execute(
                    """UPDATE score SET user_id = ?, level = ?, score_points = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?""""",
                    (score.user_id, score.level, score.score_points, score.id))
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()

    # Статический метод для удаления экземпляра класса из таблицы
    @staticmethod
    def remove(score):
        connection = make_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM score WHERE id = ?", (score.id,))
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()

    # Статический метод для удаления не законченных игр
    @staticmethod
    def cleanup():
        connection = make_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM score WHERE created_at == updated_at")
        except IntegrityError as e:
            connection.rollback()
            raise e
        connection.commit()


# Создать таблицу в момент импорта
Score.init_db()
Score.cleanup()
