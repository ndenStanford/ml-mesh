"""Register trained model."""

"""Register trained model."""

# Standard Library
import os  # Add missing import

# 3rd party libraries
import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (
    TrackedDocumentContentScoringModelCard,
    TrackedDocumentContentScoringSpecs,
)


def main() -> None:
    """Upload trained model to Neptune."""
    model_specs = TrackedDocumentContentScoringSpecs()
    model_card = TrackedDocumentContentScoringModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on Neptune AI
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
    y = df[["y"]]
    # Encode categorical features
    enc = OrdinalEncoder()
    enc.fit(X[categorical_cols])
    X[categorical_cols] = enc.transform(X[categorical_cols])
    # Split data into train and test sets
    test_size = model_card.model_params.test_size
    random_state = model_card.model_params.random_state
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    d_train = lgb.Dataset(X_train, label=y_train, categorical_feature=categorical_cols)
    d_test = lgb.Dataset(X_test, label=y_test, categorical_feature=categorical_cols)

    lgb_params = model_card.model_params.lgb_params
    num_boost_rounds = model_card.model_params.num_boost_rounds

    model = lgb.train(lgb_params, d_train, num_boost_rounds, valid_sets=[d_test])
    # Save the trained model
    model_output_path = os.path.join(model_card.local_output_dir, "trained_model.pkl")
    joblib.dump(model, model_output_path)
    # Upload trained model to Neptune
    model_version.upload_file_to_model_version(
        local_file_path=model_output_path,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # Stop tracking
    model_version.stop()


if __name__ == "__main__":
    main()
