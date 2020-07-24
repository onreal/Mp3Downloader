from datetime import datetime

from sqlalchemy import ForeignKey

from app import db


class BotLogger(db.Model):
    __tablename__ = 'botLogger'

    id = db.Column(db.Integer, primary_key=True)
    botpersonid = db.Column(db.Integer, ForeignKey("botPerson.id"), nullable=False)
    request = db.Column(db.String, nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    modifieddatetime = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, botpersonid, request, success):
        self.request = request
        self.success = success
        self.botpersonid = botpersonid
        self.modifieddatetime = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()
