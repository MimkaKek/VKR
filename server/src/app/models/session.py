from app import db

class SessionModel(db.Model):

    id      = db.Column(db.Integer,     primary_key=True)
    sid     = db.Column(db.String(128), unique=True)
    reflink = db.Column(db.String(128), unique=True)

    def __init__(self, sid: str, reflink: str) -> None:
        self.sid     = sid
        self.reflink = reflink