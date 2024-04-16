"""Class for training and managing Onclusive models."""

# Standard Library
from abc import abstractmethod

# ML libs
from transformers import EarlyStoppingCallback, Trainer, TrainingArguments

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer


class OnclusiveHuggingfaceModelTrainer(OnclusiveModelTrainer):
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSpecs): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=data_fetch_params,
        )

    @abstractmethod
    def initialize_model(self) -> None:
        """Initialize model and tokenizer.

        Example implementation
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        """
        pass

    @abstractmethod
    def data_preprocess(self) -> None:
        """Preprocess the data to the Huggingface trainer format and split for train and evaluation.

        Example implementation
        self.train_df, self.eval_df = train_test_split(
            self.dataset_df,
            test_size = 0.20,
            stratify=self.dataset_df["target_label"]
            )
        self.train_dataset = IPTCDataset(
            self.train_df,
            self.model_card.tokenizer,
            self.model_card.selected_text

        )
        self.eval_dataset = IPTCDataset(
            self.eval_df,
            self.model_card.tokenizer,
            self.model_card.level,
            self.model_card.selected_text
        )
        """
        pass

    def create_training_argument(self) -> None:
        """Create training argument object for Huggingface trainer.

        Returns: None
        """
        self.training_args = TrainingArguments(
            output_dir=self.model_card.output_dir,
            num_train_epochs=self.model_card.epochs,
            learning_rate=self.model_card.learning_rate,
            report_to="neptune",
        )

    def train(self) -> None:
        """Train the model.

        Returns: None
        """
        # using this class directly should give us tracking capability
        # https://docs.neptune.ai/integrations/transformers/
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.docs,
            tokenizer=self.tokenizer,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=1)],
        )
        self.trainer.train()

    @abstractmethod
    def predict(self) -> None:
        """Make predictions using the trained model.

        Returns: None
        """
        pass

    def optimize_model(self) -> None:
        """Optimize the model.

        Returns: None
        """
        self.train()

    @abstractmethod
    def save(self) -> None:
        """Save the trained model and related information locally.

        Returns: None
        """
        pass

    def __call__(self) -> None:
        """Call Method."""
        super(OnclusiveHuggingfaceModelTrainer, self).__call__()
        self.logger.info(
            f"Training data uploaded to s3 location : {self.full_file_key}"
        )
        self.initialize_model()
        self.optimize_model()
        self.save()
        if self.data_fetch_params.save_artifact:
            super(
                OnclusiveHuggingfaceModelTrainer, self
            ).upload_training_data_to_neptune()
