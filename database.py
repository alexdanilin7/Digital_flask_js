import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager

DB_NAME = "users.db"

@dataclass
class User:
    """Модель данных """
    id: int
    name: str
    email: str

    def to_dict(self) -> dict:
        """Сериализация в словарь для JSON"""
        return {"id": self.id, "name": self.name, "email": self.email}

class Database:
    """Класс управления БД"""
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для безопасного получения соединения"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Инициализация  БД"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            conn.commit()

    def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT id, name, email FROM users')
            return [User(**dict(row)) for row in cursor.fetchall()]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        with self.get_connection() as conn:
            row = conn.execute(
                'SELECT id, name, email FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()
            return User(**dict(row)) if row else None

    def create_user(self, name: str, email: str) -> User:
        """Создать нового пользователя"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )
            conn.commit()
            return User(id=cursor.lastrowid, name=name, email=email)