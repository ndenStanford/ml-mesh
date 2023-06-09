import requests
from app import APP_PORT, MODEL_NAME

n_pings = 100

sample = {'payload':[1,2,3]}

for i in range(n_pings):
    print(f"Pinging {i}/{n_pings}")
    requests.post(f'http://localhost:{APP_PORT}/v1/models/{MODEL_NAME}:predict',
                  json=sample)