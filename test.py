from datetime import datetime

class SessionData():
    def __init__(self) -> None:
        self.name           = ""
        self.description    = ""
        self.owner          = ""
        self.permited_users = []
        self.link           = ""
        self.last_updated   = ""
        self.created        = ""


sData = SessionData()
sData.owner   = "username"
sData.name    = "Project"
sData.created = datetime.now().strftime('%Y.%m.%d')

for item in sData.__dict__:
    print(item)
    print(sData.__dict__[item])
    
sData.__dict__["owner"] = "new name"

for item in sData.__dict__:
    print(item)
    print(sData.__dict__[item])

