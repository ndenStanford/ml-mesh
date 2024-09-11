"""Define the Visitor Estimation trainer."""


# Internal libraries
from onclusiveml.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSettings
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer

# define the IPTC model trainer as a subclass of the OnclusiveHuggingfaceModelTrainer
class VisitorEstimationTrainer(OnclusiveModelTrainer):
    """Class for training and managing Visitor Estimation models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSettings,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        # Update data_fetch_params dynamically
        self.data_fetch_params = data_fetch_params

        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=self.data_fetch_params,
        )

    def initialize_model(self) -> None:
        """Initialize model and tokenizer."""
        pass

    def create_training_argument(self) -> None:
        """Create training argument object for Huggingface trainer."""
        pass

    def data_preprocess(self) -> None:
        pass

    def train(self) -> None:
        """Train the model."""
        pass

    def predict(self, inputs: str):  # type: ignore[no-untyped-def]
        """Implement prediction logic."""
        pass

    def save(self) -> None:
        """Save the model."""
        pass

    def __call__(self) -> None:
        """Call Method."""
        super(VisitorEstimationTrainer, self).__call__()
