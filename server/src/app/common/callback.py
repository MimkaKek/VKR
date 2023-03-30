from app.common.jsonSerialized import JSONSerialized

class Callback(JSONSerialized):
    def __init__(self, status: int = 0, description: str = "Success", data: object = None) -> None:
        self.status      = status
        self.description = description
        self.data        = data