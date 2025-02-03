import sqlite3
import os.path

from development.different.global_vars import DB_DIR, DB_FILENAME


# Создать соединение к базе данных
def make_connection():
    # Создание директории, если она отсутствует
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    connection = sqlite3.connect(os.path.join(DB_DIR, DB_FILENAME))
    # Включение поддержки внешних ключей
    connection.cursor().execute("PRAGMA foreign_keys = on")
    return connection
