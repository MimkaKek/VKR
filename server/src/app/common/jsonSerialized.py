import json

class JSONSerialized:
    
    def __init__(self) -> None:
        pass
    
    def dump(self) -> str:
        return json.dumps(self.__dict__)
    
    def load(self, jsonData: str) -> None:
        self.__dict__ = json.loads(jsonData)
            