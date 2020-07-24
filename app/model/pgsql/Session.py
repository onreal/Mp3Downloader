from passlib.apps import custom_app_context as pwd_context

from app import db


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_bls_session(cls, session):
        query = cls.query.filter_by(session=session).first()
        return bool(query)
