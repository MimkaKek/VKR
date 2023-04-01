from app.common.jsonSerialized import JSONSerialized
from datetime import datetime

class ProjectData(JSONSerialized):
    def __init__(self, name: str = "", desc: str = "", owner: str = "",
                 permittedUsers: list[str] = [], isPublic: bool = False, isTemplate: bool = False,
                 created: str = datetime.now().strftime('%Y.%m.%d %H:%M:%S'),
                 lastUpdated: str = datetime.now().strftime('%Y.%m.%d %H:%M:%S')) -> None:
        
        self.name           = name
        self.description    = desc
        self.owner          = owner
        self.permitedUsers  = permittedUsers
        self.isPublic       = isPublic
        self.isTemplate     = isTemplate
        self.created        = created
        self.lastUpdated    = lastUpdated