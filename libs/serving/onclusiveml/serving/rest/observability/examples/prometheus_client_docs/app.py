# single worker procecss
# from fastapi import FastAPI
# from prometheus_client import make_asgi_app

# 3rd party libraries
# # Create app
# app = FastAPI(debug=False)
# # Add prometheus asgi middleware to route /metrics requests
# metrics_app = make_asgi_app()
# app.mount("/metrics", metrics_app)
from fastapi import FastAPI
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    generate_latest,
    make_asgi_app,
    multiprocess,
)


app = FastAPI(debug=False)

MY_COUNTER = Counter("my_counter", "Description of my counter")
# Expose metrics.
def make_metrics_app(environ, start_response):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    status = "200 OK"
    response_headers = [
        ("Content-type", CONTENT_TYPE_LATEST),
        ("Content-Length", str(len(data))),
    ]
    start_response(status, response_headers)
    return iter([data])


metrics_app = make_metrics_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
