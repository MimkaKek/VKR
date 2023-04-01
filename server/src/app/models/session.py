from app import db

class ProjectModel(db.Model):

    id      = db.Column(db.Integer,     primary_key=True)
    pid     = db.Column(db.String(128), unique=True)
    reflink = db.Column(db.String(128), unique=True)

    def __init__(self, pid: str, reflink: str) -> None:
        self.pid     = pid
        self.reflink = reflink