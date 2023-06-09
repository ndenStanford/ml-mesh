
# Standard Library
import random
from pathlib import Path

# 3rd party libraries
import uvicorn
from fastapi import FastAPI, Request, Response
from instrumentator import instrumentator
from prometheus_client import REGISTRY, exposition


ROOT_DIR = Path(__file__).parent.parent

# 3rd party libraries
import uvicorn
from pydantic import BaseModel, Field


METRICS_PORT = 8000
APP_PORT = 8001
expose_app = False

feature_names = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol_pct_vol",
]


class Wine(BaseModel):
    fixed_acidity: float = Field(
        ..., ge=0, description="grams per cubic decimeter of tartaric acid"
    )
    volatile_acidity: float = Field(
        ..., ge=0, description="grams per cubic decimeter of acetic acid"
    )
    citric_acid: float = Field(
        ..., ge=0, description="grams per cubic decimeter of citric acid"
    )
    residual_sugar: float = Field(
        ..., ge=0, description="grams per cubic decimeter of residual sugar"
    )
    chlorides: float = Field(
        ..., ge=0, description="grams per cubic decimeter of sodium chloride"
    )
    free_sulfur_dioxide: float = Field(
        ..., ge=0, description="milligrams per cubic decimeter of free sulfur dioxide"
    )
    total_sulfur_dioxide: float = Field(
        ..., ge=0, description="milligrams per cubic decimeter of total sulfur dioxide"
    )
    density: float = Field(..., ge=0, description="grams per cubic meter")
    ph: float = Field(
        ..., ge=0, lt=14, description="measure of the acidity or basicity"
    )
    sulphates: float = Field(
        ..., ge=0, description="grams per cubic decimeter of potassium sulphate"
    )
    alcohol_pct_vol: float = Field(
        ..., ge=0, le=100, description="alcohol percent by volume"
    )


class Rating(BaseModel):
    quality: float = Field(
        ...,
        ge=0,
        le=10,
        description="wine quality grade ranging from 0 (very bad) to 10 (excellent)",
    )


app = FastAPI()
# neither approach works when using more than 1 uvicorn worker
# the metrics endpoints only seem to show metrics collected/created by that specific worker,
# but not both
if expose_app:
    instrumentator.instrument(app).expose(
        app, include_in_schema=False, should_gzip=True
    )
else:

    instrumentator.instrument(app)

    @app.get("/metrics")
    async def metrics_handler(request: Request) -> Response:
        encoder, content_type = exposition.choose_encoder(request.headers.get("accept"))
        return Response(
            content=encoder(REGISTRY), headers={"content-type": content_type}
        )


@app.get("/")
async def root():
    return "Wine Quality Ratings"


@app.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine):
    sample_dict = sample.dict()
    prediction = random.random() * 10
    response.headers["X-model-score"] = str(prediction)
    return Rating(quality=prediction)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=APP_PORT, workers=2)
