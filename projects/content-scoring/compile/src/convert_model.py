"""Compile trained model."""

# 3rd party libraries
import joblib
from hummingbird.ml import convert

# Source
from src.settings import CompiledTrackedModelSpecs  # type: ignore[attr-defined]


def convert_model() -> None:
    """Converting format to the right model (torch)."""
    settings = CompiledTrackedModelSpecs()

    input_model_path = settings.input_dir
    output_model_path = settings.output_dir
    target_format = settings.target_format

    model = joblib.load(input_model_path)

    converted_model = convert(model, target_format)

    converted_model.save(output_model_path)


if __name__ == "__main__":
    convert_model()
