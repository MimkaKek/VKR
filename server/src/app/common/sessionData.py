from app.common.jsonSerialized import JSONSerialized

class SessionData(JSONSerialized):
    def __init__(self) -> None:
        self.name           = ""
        self.description    = ""
        self.owner          = ""
        self.link           = ""
        self.permitedUsers  = []
        self.lastUpdated    = ""
        self.created        = ""