import uuid
from datetime import datetime

from src.common.database import Database


class Entry(object):

    def __init__(self, user_id, title, content, date_event, _id=None):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.date_event = date_event
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date_last_modified = datetime.now()

    @staticmethod
    def edit_entry(entry_id, update):
        Database.update_one('entries', {"_id":entry_id}, update)

    @staticmethod
    def get_entries_by_user_id(user_id):
        return [entry for entry in Database.find('entries', {"user_id": user_id})]

    @staticmethod
    def get_entry_by_id(entry_id):
        return Database.find('entries', {"_id": entry_id})

    @staticmethod
    def delete_entry_by_id(entry_id):
        Database.remove_one('entries', {"_id": entry_id})

    def json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "date_event": self.date_event,
            "date_last_modified": self.date_last_modified
        }

    def save_to_db(self):
        Database.insert('entries', self.json())