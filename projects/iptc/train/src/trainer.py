"""Define the IPTC trainer."""

# Standard Library
import os

# ML libs
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)
from transformers.integrations import NeptuneCallback

# 3rd party libraries
from pandas import DataFrame
from sklearn.model_selection import train_test_split

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs
from onclusiveml.training.huggingface.trainer import (
    OnclusiveHuggingfaceModelTrainer,
)
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer

# Source
from src.class_dict import (
    CLASS_DICT_SECOND,
    CLASS_DICT_THIRD,
    ID_TO_LEVEL,
    ID_TO_TOPIC,
)
from src.dataset import IPTCDataset
from src.utils import (
    compute_metrics,
    extract_model_id,
    find_category_for_subcategory,
    find_num_labels,
    topic_conversion,
)


# define the IPTC model trainer as a subclass of the OnclusiveHuggingfaceModelTrainer
class IPTCTrainer(OnclusiveHuggingfaceModelTrainer):
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
        self.model_id = extract_model_id(tracked_model_specs.project)
        self.level = ID_TO_LEVEL[self.model_id]
        self.iptc_label = ID_TO_TOPIC[self.model_id]
        # Update data_fetch_params dynamically
        self.data_fetch_params = data_fetch_params
        data_fetch_configurations = {
            1: {
                "entity_name": "iptc_first_level",
                "feature_view_name": "iptc_first_level_feature_view",
                "redshift_table": "iptc_first_level",
                "filter_columns": [],
                "filter_values": [],
                "comparison_operators": [],
                "non_nullable_columns": [
                    model_card.model_params.selected_text,
                    "topic_1",
                ],
            },
            2: {
                "entity_name": "iptc_second_level",
                "feature_view_name": "iptc_second_level_feature_view",
                "redshift_table": "iptc_second_level",
                "filter_columns": ["topic_1"],
                "filter_values": [self.iptc_label],
                "comparison_operators": ["equal"],
                "non_nullable_columns": [
                    model_card.model_params.selected_text,
                    "topic_1",
                    "topic_2",
                ],
            },
            3: {
                "entity_name": "iptc_third_level",
                "feature_view_name": "iptc_third_level_feature_view",
                "redshift_table": "iptc_third_level",
                "filter_columns": ["topic_2"],
                "filter_values": [self.iptc_label],
                "comparison_operators": ["equal"],
                "non_nullable_columns": [
                    model_card.model_params.selected_text,
                    "topic_1",
                    "topic_2",
                    "topic_3",
                ],
            },
        }
        for key, value in data_fetch_configurations[self.level].items():
            setattr(self.data_fetch_params, key, value)

        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=self.data_fetch_params,
        )

    def initialize_model(self) -> None:
        """Initialize model and tokenizer."""
        if self.level == 1:
            self.first_level_root = None
            self.second_level_root = None
        elif self.level == 2:
            self.first_level_root = self.iptc_label
            self.second_level_root = None
        elif self.level == 3:
            self.second_level_root = self.iptc_label
            self.first_level_root = find_category_for_subcategory(
                CLASS_DICT_SECOND, self.second_level_root
            )
        self.model_name = self.model_card.model_params.model_name
        self.num_labels = find_num_labels(
            self.level,
            self.first_level_root,
            self.second_level_root,
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, num_labels=self.num_labels
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def create_training_argument(self) -> None:
        """Create training argument object for Huggingface trainer."""
        self.training_args = TrainingArguments(
            output_dir=self.model_card.local_output_dir,
            num_train_epochs=self.model_card.model_params.epochs,
            learning_rate=self.model_card.model_params.learning_rate,
            per_device_train_batch_size=self.model_card.model_params.train_batch_size,
            per_device_eval_batch_size=self.model_card.model_params.eval_batch_size,
            warmup_steps=self.model_card.model_params.warmup_steps,
            report_to=self.model_card.model_params.report_to,
            evaluation_strategy=self.model_card.model_params.evaluation_strategy,
            save_strategy=self.model_card.model_params.save_strategy,
            save_steps=self.model_card.model_params.save_steps,
            save_total_limit=self.model_card.model_params.save_total_limit,
            load_best_model_at_end=self.model_card.model_params.load_best_model_at_end,
        )

    def data_preprocess(self) -> None:
        """Preprocess to torch dataset and split for train and evaluation."""
        self.dataset_df: DataFrame = self.dataset_df.dropna(
            subset=self.data_fetch_params.non_nullable_columns
        )  # type: ignore

        # Log the size and class distribution after dropping nulls
        num_datapoints = len(self.dataset_df)
        self.logger.info(f"Number of datapoints after dropping nulls: {num_datapoints}")
        class_distribution = self.dataset_df[f"topic_{self.level}"].value_counts(
            normalize=True
        )
        self.logger.info(
            f"Class distribution after dropping nulls: \n{class_distribution}"
        )

        if self.data_fetch_params.redshift_table == "iptc_first_level":
            self.dataset_df = self.dataset_df[
                self.dataset_df["topic_1"].isin(CLASS_DICT_SECOND.keys())
            ]

        if self.data_fetch_params.redshift_table == "iptc_second_level":
            self.dataset_df = self.dataset_df[
                self.dataset_df["topic_2"].isin(CLASS_DICT_THIRD.keys())
            ]

        if self.data_fetch_params.redshift_table == "iptc_third_level":
            self.dataset_df = self.dataset_df[
                self.dataset_df["topic_3"].isin(
                    [j for i in CLASS_DICT_THIRD.values() for j in i.values()]
                )
            ]
        # fix the topic discrepencies
        self.dataset_df = topic_conversion(self.dataset_df)
        try:
            # train eval split
            self.train_df, self.eval_df = train_test_split(
                self.dataset_df,
                test_size=self.model_card.model_params.test_size,
                stratify=self.dataset_df[f"topic_{self.level}"],
            )
        except Exception as e:
            self.logger.info(f"Error with stratify splitting: {e}")
            # train eval split
            self.train_df, self.eval_df = train_test_split(
                self.dataset_df,
                test_size=self.model_card.model_params.test_size,
            )
        # convert df to torch dataset
        self.train_dataset = IPTCDataset(
            self.train_df,
            self.tokenizer,
            self.level,
            self.model_card.model_params.selected_text,
            self.first_level_root,
            self.second_level_root,
            self.model_card.model_params.max_length,
        )
        self.eval_dataset = IPTCDataset(
            self.eval_df,
            self.tokenizer,
            self.level,
            self.model_card.model_params.selected_text,
            self.first_level_root,
            self.second_level_root,
            self.model_card.model_params.max_length,
        )

    def train(self) -> None:
        """Train the model."""
        # using this class directly should give us tracking capability
        # https://docs.neptune.ai/integrations/transformers/
        self.create_training_argument()
        self.data_preprocess()
        self.logger.info(f"Training arguments : {self.training_args}")

        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            compute_metrics=compute_metrics,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            tokenizer=self.tokenizer,
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=self.model_card.model_params.early_stopping_patience
                )
            ],
        )
        self.trainer.train()

    def predict(self, inputs: str):  # type: ignore[no-untyped-def]
        """Implement prediction logic."""
        prediction = self.trainer.predict(inputs)
        return prediction

    def save(self) -> None:
        """Save the model."""
        self.iptc_model_local_dir = os.path.join(
            self.model_card.local_output_dir, f"{self.tracked_model_specs.model}"
        )
        self.trainer.save_model(self.iptc_model_local_dir)

    def __call__(self) -> None:
        """Call Method."""
        super(IPTCTrainer, self).__call__()

        if self.data_fetch_params.save_artifact:
            sample_df = self.dataset_df.sample(15)

            sample_docs = sample_df[
                self.model_card.model_params.selected_text
            ].values.tolist()

            sample_dataset = IPTCDataset(
                sample_df,
                self.tokenizer,
                self.level,
                self.model_card.model_params.selected_text,
                self.first_level_root,
                self.second_level_root,
                self.model_card.model_params.max_length,
            )
            sample_predictions = self.predict(sample_dataset)

            neptune_run = NeptuneCallback.get_run(self.trainer).get_url()

            super(OnclusiveModelTrainer, self).__call__(
                [
                    sample_docs,
                    self.model_card.model_params.dict(),
                    {
                        "probs": sample_predictions[0].tolist(),
                        "labels": sample_predictions[1].tolist(),
                        "neptune_run": neptune_run,
                    },
                ],
                [
                    self.model_card.model_test_files.inputs,
                    self.model_card.model_test_files.inference_params,
                    self.model_card.model_test_files.predictions,
                ],
                self.iptc_model_local_dir,
            )
