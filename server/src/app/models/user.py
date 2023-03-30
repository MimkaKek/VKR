from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):

    id            = db.Column(db.Integer,     primary_key=True)
    username      = db.Column(db.String(80),  unique=True     )
    email         = db.Column(db.String(120), unique=True     )
    password_hash = db.Column(db.String(128)                  )
    role          = db.Column(db.Integer                      )

    def __init__(self, email: str, username: str, password: str, role: str) -> None:
        self.email         = email
        self.username      = username
        self.password_hash = generate_password_hash(password)
        self.role          = role

    def SetPassword(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def CheckPassword(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)