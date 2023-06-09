from kserve import Model, ModelServer
from typing import Dict

N_WORKERS = 2
APP_PORT = 8000
MODEL_NAME = 'kserve-example'

class ExampleModel(Model):
    
    def __init__(self, name: str):
       super().__init__(name)
       self.name = name
       self.load()

    def load(self):
        self.ready = True

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        
        return payload
    
if __name__ == "__main__":
    model = ExampleModel(MODEL_NAME)
    model.load()
    # this also only captures metrics from the respective worker process
    ModelServer(workers=N_WORKERS,http_port=APP_PORT).start([model])