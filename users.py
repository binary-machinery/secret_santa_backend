from dataclasses import dataclass

from flask_login import UserMixin

import database


@dataclass
class User(UserMixin):
    user_id: int
    email: str
    name: str
    password_hash: str

    def __init__(self, user_id: int, email: str, name: str, password_hash: str):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password_hash = password_hash

    def get_id(self):
        return self.user_id


class Users:
    def __init__(self, db_filename):
        self.database = database.DatabaseWrapper(db_filename)
        self.database.execute('CREATE TABLE IF NOT EXISTS users ('
                              'id INTEGER PRIMARY KEY, '
                              'email TEXT UNIQUE, '
                              'name TEXT, '
                              'password_hash TEXT)')

    def get_database_wrapper(self):
        return self.database

    def add_user(self, email, password_hash):
        if not email or not password_hash:
            print('Users::add_user: impossible to add a user with the empty parameter!')
            return

        self.database.execute('INSERT INTO users (email, password_hash) '
                              'VALUES (?, ?)',
                              (email, password_hash))

    def set_name(self, user_id, name):
        self.database.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))

    def get_user_by_id(self, user_id):
        res = self.database.execute_and_fetch(
            'SELECT id, email, name, password_hash FROM users WHERE id = ?',
            (user_id,)
        )
        return User(res[0][0], res[0][1], res[0][2], res[0][3])

    def get_user_by_email(self, email):
        res = self.database.execute_and_fetch(
            'SELECT id, email, name, password_hash FROM users WHERE email = ?',
            (email,)
        )
        return User(res[0][0], res[0][1], res[0][2], res[0][3])

    def delete_user(self, user_id):
        self.database.execute('DELETE FROM users WHERE id = ?', (user_id,))
