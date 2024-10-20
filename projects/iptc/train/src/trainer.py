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
from onclusiveml.feature_store.settings import FeastFeatureStoreSettings
from onclusiveml.tracking import TrackedModelCard, TrackedModelSettings
from onclusiveml.training.huggingface.trainer import (
    OnclusiveHuggingfaceModelTrainer,
)
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer

# Source
from src.class_dict import (
    CANDIDATE_DICT_FIRST,
    CANDIDATE_DICT_FOURTH,
    CANDIDATE_DICT_SECOND,
    CANDIDATE_DICT_THIRD,
    ID_TO_LEVEL,
    ID_TO_TOPIC,
)
from src.dataset import IPTCDataset
from src.name_mapping_dict import (
    NAME_MAPPING_DICT_FIRST,
    NAME_MAPPING_DICT_SECOND,
    NAME_MAPPING_DICT_THIRD,
)
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
        tracked_model_specs: TrackedModelSettings,
        model_card: TrackedModelCard,
        data_fetch_params: FeastFeatureStoreSettings,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSettings): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeastFeatureStoreSettings): Parameters for fetching data from feature store.

        Returns: None
        """
        self.model_id = extract_model_id(tracked_model_specs.project)
        self.level = ID_TO_LEVEL[self.model_id]
        self.iptc_label = ID_TO_TOPIC[self.model_id]
        # Reverse the keys and values of both dictionaries
        reversed_name_mapping_first = {v: k for k, v in NAME_MAPPING_DICT_FIRST.items()}
        reversed_name_mapping_second = {
            v: k for k, v in NAME_MAPPING_DICT_SECOND.items()
        }
        reversed_name_mapping_third = {v: k for k, v in NAME_MAPPING_DICT_THIRD.items()}
        if self.iptc_label in reversed_name_mapping_first.keys():
            filtered_value = reversed_name_mapping_first[self.iptc_label]
        elif self.iptc_label in reversed_name_mapping_second.keys():
            filtered_value = reversed_name_mapping_second[self.iptc_label]
        elif self.iptc_label in reversed_name_mapping_third.keys():
            filtered_value = reversed_name_mapping_third[self.iptc_label]
        else:
            filtered_value = self.iptc_label
        # Access the is_on_demand flag from data_fetch_params
        self.is_on_demand = data_fetch_params.is_on_demand
        # Update data_fetch_params dynamically
        self.data_fetch_params = data_fetch_params
        data_fetch_configurations = {
            1: {
                "entity_df": """ SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "features"."pred_iptc_first_level" """,
                "features": [
                    "iptc_first_level:topic_1",
                    "iptc_first_level:content",
                    "iptc_first_level:title",
                    "iptc_first_level_on_demand_feature_view:topic_1_llm",
                ],
            },
            2: {
                "entity_df": f"""SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp
                                FROM "features"."pred_iptc_second_level"
                                WHERE topic_1 = '{filtered_value}' """,
                "features": [
                    "iptc_second_level:topic_1",
                    "iptc_second_level:topic_2",
                    "iptc_second_level:content",
                    "iptc_second_level:title",
                    "iptc_second_level_on_demand_feature_view:topic_2_llm",
                ],
            },
            3: {
                "entity_df": f"""SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp
                                FROM "features"."pred_iptc_third_level"
                                WHERE topic_2 = '{filtered_value}' """,
                "features": [
                    "iptc_third_level:topic_1",
                    "iptc_third_level:topic_2",
                    "iptc_third_level:topic_3",
                    "iptc_third_level:content",
                    "iptc_third_level:title",
                    "iptc_third_level_on_demand_feature_view:topic_3_llm",
                ],
            },
            4: {
                "entity_df": f"""SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp
                                FROM "features"."pred_iptc_third_level"
                                WHERE topic_3 = '{filtered_value}' """,
                "features": [
                    "iptc_third_level:topic_1",
                    "iptc_third_level:topic_2",
                    "iptc_third_level:topic_3",
                    "iptc_third_level:content",
                    "iptc_third_level:title",
                    "iptc_fourth_level_on_demand_feature_view:topic_4_llm",
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

    def get_candidate_list(self, level: int) -> list:
        """Generate a list of candidate names based on the input level.

        Args:
            level (int): The level of categorization (1, 2, 3, or 4).

        Returns:
            list: A list of candidate names.
        """
        if level == 1:
            candidate_list = [
                category["name"] for category in CANDIDATE_DICT_FIRST["root"].values()
            ]
        elif level == 2:
            candidate_list = [
                category["name"]
                for category in CANDIDATE_DICT_SECOND[self.iptc_label].values()
            ]
        elif level == 3:
            candidate_list = [
                category["name"]
                for category in CANDIDATE_DICT_THIRD[self.iptc_label].values()
            ]
        elif level == 4:
            candidate_list = [
                category["name"]
                for category in CANDIDATE_DICT_FOURTH[self.iptc_label].values()
            ]

        return candidate_list

    def initialize_model(self) -> None:
        """Initialize model and tokenizer."""
        if self.level == 1:
            self.first_level_root = None
            self.second_level_root = None
            self.third_level_root = None
        elif self.level == 2:
            self.first_level_root = self.iptc_label
            self.second_level_root = None
            self.third_level_root = None
        elif self.level == 3:
            self.third_level_root = None
            self.second_level_root = self.iptc_label
            self.first_level_root = find_category_for_subcategory(
                CANDIDATE_DICT_SECOND, self.second_level_root
            )
        elif self.level == 4:
            self.third_level_root = self.iptc_label
            self.second_level_root = find_category_for_subcategory(
                CANDIDATE_DICT_THIRD, self.third_level_root
            )
            self.first_level_root = find_category_for_subcategory(
                CANDIDATE_DICT_SECOND, self.second_level_root
            )
        self.model_name = self.model_card.model_params.model_name
        self.num_labels = find_num_labels(
            self.level,
            self.first_level_root,
            self.second_level_root,
            self.third_level_root,
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
        # drop null
        # self.dataset_df: DataFrame = self.dataset_df.dropna(
        #     subset=self.data_fetch_params.non_nullable_columns
        # )  # type: ignore
        self.dataset_df: DataFrame = self.dataset_df.dropna()
        print(self.dataset_df.columns)
        print(self.dataset_df.iloc[0])
        # Filter out rows with invalid labels not in the candidate list
        self.logger.info("Filtering rows with invalid labels...")
        valid_labels = self.get_candidate_list(
            level=self.level
        )  # Implement this method to return the candidate dictionary
        column_name = (
            f"topic_{self.level}_llm" if self.is_on_demand else f"topic_{self.level}"
        )

        initial_row_count = len(self.dataset_df)
        self.logger.info(f"Initial dataset size: {self.dataset_df.shape}")
        # Apply the filter
        self.dataset_df = self.dataset_df[
            self.dataset_df[column_name].isin(valid_labels)
        ]
        # Log the size after removing invalid labels
        filtered_row_count = len(self.dataset_df)
        removed_rows = initial_row_count - filtered_row_count
        self.logger.info(
            f"Removed {removed_rows} rows with invalid labels. Filtered dataset size: {self.dataset_df.shape}"
        )

        if filtered_row_count == 0:
            self.logger.warning(
                "No valid rows remaining after filtering. Please check the input data or candidate list."
            )
        # Display the first few rows of the filtered dataset
        self.logger.info(f"Final preprocessed dataset:\n{self.dataset_df.head()}")
        # fix the topic discrepencies
        self.dataset_df = topic_conversion(self.dataset_df)
        # self.dataset_df = self.dataset_df.sample(n=50, random_state=42)
        # Log the size and class distribution after dropping nulls
        num_datapoints = len(self.dataset_df)
        self.logger.info(f"Number of datapoints after dropping nulls: {num_datapoints}")
        class_distribution = self.dataset_df[column_name].value_counts(normalize=True)
        self.logger.info(
            f"Class distribution after dropping nulls: \n{class_distribution}"
        )
        # train eval split
        try:
            self.train_df, self.eval_df = train_test_split(
                self.dataset_df,
                test_size=self.model_card.model_params.test_size,
                stratify=self.dataset_df[f"topic_{self.level}"],
            )
        except Exception as e:
            self.logger.info(f"Error with stratify splitting: {e}")
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
            self.third_level_root,
            self.model_card.model_params.max_length,
            is_on_demand=self.is_on_demand,  # Pass the on-demand flag
        )
        self.eval_dataset = IPTCDataset(
            self.eval_df,
            self.tokenizer,
            self.level,
            self.model_card.model_params.selected_text,
            self.first_level_root,
            self.second_level_root,
            self.third_level_root,
            self.model_card.model_params.max_length,
            is_on_demand=self.is_on_demand,  # Pass the on-demand flag
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
            self.model_card.local_output_dir, f"{self.tracked_model_settings.model}"
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
                self.third_level_root,
                self.model_card.model_params.max_length,
                is_on_demand=self.is_on_demand,  # Pass the on-demand flag
            )
            sample_predictions = self.predict(sample_dataset)

            neptune_run = NeptuneCallback.get_run(self.trainer).get_url()

            super(OnclusiveModelTrainer, self).__call__(
                [
                    sample_docs,
                    self.model_card.model_params.model_dump(),
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
