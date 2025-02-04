from development.db.db import make_connection


# Вспомогательный класс для отображения результатов
class ScoreReport:
    # Инициализация класса
    def __init__(self, id=None, user_nickname=None, level=None, score_points=None, created_at=None, updated_at=None):
        self.id = id  # Идентификатор записи
        self.user_nickname = user_nickname  # Идентификатор записи в таблице users
        self.level = level  # Номер уровня
        self.score_points = score_points  # Количество набранных очков
        self.created_at = created_at  # Время создания записи
        self.updated_at = updated_at  # Время изменения записи

    # Статический метод для получения записи таблиц score и user по user_id и level в виде экземпляров класса
    @staticmethod
    def get(user_id=None, level=None, limit=None):
        args = []
        where_str = []
        limit_str = ""
        if user_id is not None:
            args.append(user_id)
            where_str.append("u.id = ?")
        if level is not None:
            args.append(level)
            where_str.append("s.level = ?")
        if limit is not None:
            args.append(limit)
            limit_str = " LIMIT ?"
        if len(where_str):
            where_str.append("")
        records = []
        cursor = make_connection().cursor()
        cursor.execute(
            f"""SELECT s.id, u.nickname, s.level, s.score_points, s.created_at, s.updated_at 
            FROM score s join user u on s.user_id = u.id 
            WHERE {" and ".join(where_str)}s.created_at != s.updated_at 
            ORDER BY s.score_points DESC, s.created_at ASC{limit_str}""",
            args)
        for i in cursor.fetchall():
            records.append(ScoreReport(*i))
        return records
