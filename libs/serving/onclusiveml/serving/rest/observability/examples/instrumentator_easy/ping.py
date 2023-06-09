import requests
from app import Wine

sample = Wine(
    fixed_acidity=0.1,
    volatile_acidity=1,
    citric_acid=2,
    residual_sugar=0.5,
    chlorides=1,
    free_sulfur_dioxide=1,
    total_sulfur_dioxide=1,
    density=1,
    ph=1,
    sulphates=1,
    alcohol_pct_vol=1
)

n_pings = 100

for i in range(n_pings):
    print(f"Pinging {i}/{n_pings}")
    requests.post('http://localhost:8001/predict',
                  json=sample.dict())