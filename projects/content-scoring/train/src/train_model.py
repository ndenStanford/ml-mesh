"""Register trained model."""

# Standard Library
import os

# 3rd party libraries
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedDocumentContentScoringModelCard,
    TrackedDocumentContentScoringSpecs,
)


def main() -> None:
    """Train and upload a model to Neptune AI."""
    # Initialize model specs and model card
    model_specs = TrackedDocumentContentScoringSpecs()
    model_card = TrackedDocumentContentScoringModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # Initialize registered model on Neptune AI
    model_version = TrackedModelVersion(**model_specs.dict())
    # Load data
    data_file_path = model_card.model_params.data_file_path
    df = pd.read_parquet(data_file_path)
    # Preprocess data
    df["y"] = 1
    df.loc[
        df["message_type"] == "onclusive.delivery.event.content.validation.accepted",
        "y",
    ] = 1
    df.loc[
        df["message_type"] == "onclusive.delivery.event.content.validation.rejected",
        "y",
    ] = 0

    numerical_cols = model_card.model_params.numerical_cols
    categorical_cols = model_card.model_params.categorical_cols
    X = df[numerical_cols + categorical_cols]
    y = df["y"]
    # Encode categorical features
    enc = OrdinalEncoder()
    X[categorical_cols] = enc.fit_transform(X[categorical_cols])
    # Split data into train and test sets
    test_size = model_card.model_params.test_size
    random_state = model_card.model_params.random_state
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    rf_params = model_card.model_params.rf_params
    model = RandomForestClassifier(**rf_params)
    model.fit(X_train, y_train)

    # Save the trained model
    model_output_path_pkl = os.path.join(
        model_card.local_output_dir, "compiled_model.pkl"
    )
    joblib.dump(model, model_output_path_pkl)
    # Upload trained model file to Neptune
    model_version.upload_file_to_model_version(
        local_file_path=model_output_path_pkl,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )

    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )
    # Stop tracking
    model_version.stop()


if __name__ == "__main__":
    main()
