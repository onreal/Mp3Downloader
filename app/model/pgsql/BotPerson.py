from datetime import datetime

from app import db


def update():
    db.session.commit()


class BotPerson(db.Model):
    __tablename__ = 'botPerson'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=True)
    socialId = db.Column(db.String(), nullable=False)
    platform = db.Column(db.String(), nullable=False)
    modifieddatetime = db.Column(db.TIMESTAMP, nullable=False)
    chatid = db.Column(db.Integer, nullable=True)

    def __init__(self, dict_info):
        self.name = dict_info['name']
        self.surname = dict_info['surname']
        self.username = dict_info['username']
        self.socialId = dict_info['socialId']
        self.platform = dict_info['platform']
        self.modifieddatetime = datetime.now()
        self.chatid = dict_info['chatid']

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()
