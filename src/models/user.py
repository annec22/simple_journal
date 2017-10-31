import uuid
from datetime import datetime

from flask import session

from src.common.database import Database
from src.models.entry import Entry


class User(object):
    def __init__(self, name, username, email, password, _id=None):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_user_by_username(cls, username):
        user = Database.find_one('users', {'username': username})
        if user is not None:
            print(user)
            return cls(**user)

    @classmethod
    def register_user(cls, name, username, email, password):
        user = cls.get_user_by_username(username)
        if user is None:
            new_user = cls(name, username, email, password)
            new_user.save_to_db()
            session['username'] = username
            return True
        else:
            return False # username or email already exists

    @staticmethod
    def is_valid_login(username, password):
        user = User.get_user_by_username(username)
        if user is not None:
            return user.password == password
        else:
            return False

    @staticmethod
    def login_user(username):
        session['username'] = username

    @staticmethod
    def logout():
        session['username'] = None

    def get_user_entries_by_user_id(self):
        return Entry.get_entries_by_user_id(self._id)

    @staticmethod
    def get_user_entry_by_id(entry_id):
        return Entry.get_entry_by_id(entry_id)

    def new_entry(self, user_id, title, content, date_event):
        new_entry = Entry(user_id, title, content, date_event)
        new_entry.save_to_db()

    @staticmethod
    def edit_entry_by_id(entry_id, title, content, date_event):
        update = {
                    { "$set": {"title": title} },
                    { "$set":{"content": content} },
                    { "$set": {"date_event": date_event} },
                    { "$set": {"date_last_modified": datetime.now()} }
        }

        Entry.edit_entry(entry_id, update)

    @staticmethod
    def remove_entry_by_id(entry_id):
        Entry.delete_entry_by_id(entry_id)

    def json(self):
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_db(self):
        Database.insert('users', self.json())


