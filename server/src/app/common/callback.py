from app.common.jsonSerialized import JSONSerialized

class Callback(JSONSerialized):
    def __init__(self, status: bool = True, data: object = None) -> None:
        self.status = status
        self.data   = data
        pass