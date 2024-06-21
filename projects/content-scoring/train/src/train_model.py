"""Register trained model."""

# Standard Library
import os

# 3rd party libraries
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedDocumentContentScoringModelCard,
    TrackedDocumentContentScoringSpecs,
    TrackedDocumentUncompiledContentScoringSpecs,
)


def main() -> None:
    """Train and upload a model to Neptune AI."""
    # Initialize model specs and model card
    model_specs = TrackedDocumentContentScoringSpecs()
    uncompiled_model_specs = TrackedDocumentUncompiledContentScoringSpecs()
    model_card = TrackedDocumentContentScoringModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # Initialize registered model on Neptune AI
    model_version = TrackedModelVersion(**model_specs.model_dump())
    uncompiled_model_version = TrackedModelVersion(
        **uncompiled_model_specs.model_dump()
    )
    # Load data
    X_dict = uncompiled_model_version.download_config_from_model_version(
        neptune_attribute_path=model_card.model_test_files.inputs
    )
    y_dict = uncompiled_model_version.download_config_from_model_version(
        neptune_attribute_path=model_card.model_test_files.predictions
    )
    X = pd.DataFrame.from_dict(X_dict, orient="index")
    y = pd.DataFrame.from_dict(y_dict, orient="index")
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
        config=model_card.model_dump(), neptune_attribute_path="model/model_card"
    )

    for (test_file, test_file_attribute_path) in [
        (X_dict, model_card.model_test_files.inputs),
        (y_dict, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )

    # Stop tracking
    model_version.stop()


if __name__ == "__main__":
    main()
