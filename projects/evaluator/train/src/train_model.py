"""Register trained model."""

# 3rd party libraries
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

# Source
from src.settings import DocumentEvaluatorParams


def main() -> None:
    """Train and evaluate the model."""
    params = DocumentEvaluatorParams()

    data_file_path = params.data_file_path
    df = pd.read_parquet(data_file_path)

    df["y"] = 1
    df.loc[
        df["message_type"] == "onclusive.delivery.event.content.validation.accepted",
        "y",
    ] = 1
    df.loc[
        df["message_type"] == "onclusive.delivery.event.content.validation.rejected",
        "y",
    ] = 0

    numerical_cols = params.numerical_cols
    categorical_cols = params.categorical_cols
    X = df[numerical_cols + categorical_cols]
    y = df[["y"]]
    # Encode categorical features
    enc = OrdinalEncoder()
    enc.fit(X[categorical_cols])
    X[categorical_cols] = enc.transform(X[categorical_cols])

    test_size = params.test_size
    random_state = params.random_state
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    d_train = lgb.Dataset(X_train, label=y_train, categorical_feature=categorical_cols)
    d_test = lgb.Dataset(X_test, label=y_test, categorical_feature=categorical_cols)

    lgb_params = params.lgb_params
    num_boost_rounds = params.num_boost_rounds

    model = lgb.train(lgb_params, d_train, num_boost_rounds, valid_sets=[d_test])
    model.save_model("data/model")


if __name__ == "__main__":
    main()
