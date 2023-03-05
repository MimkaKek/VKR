from app import db

class TemplateModel(db.Model):

    id      = db.Column(db.Integer,     primary_key=True)
    tid     = db.Column(db.String(128), unique=True)
    reflink = db.Column(db.String(128), unique=True)

    def __init__(self, tid: str, reflink: str) -> None:
        self.tid     = tid
        self.reflink = reflink