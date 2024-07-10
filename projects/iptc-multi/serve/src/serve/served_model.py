"""Prediction model."""

# Standard Library
import random
import re
import time
from typing import Any, Dict, List, Set, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.iptc.class_dict import (
    AVAILABLE_MODELS,
    CLASS_DICT_SECOND,
    CLASS_DICT_THIRD,
    CONVERSION_DICT,
    DROP_LIST,
    TOPIC_TO_ID,
)
from onclusiveml.nlp.language import filter_language
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.serving.client import OnclusiveApiClient
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()
logger = get_default_logger(__name__)


class ServedIPTCMultiModel(ServedModel):
    """Served IPTC Multi model."""

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="iptc-multi")
        self.last_checked: Dict[str, float] = {}
        self.last_failed: Set[str] = set()
        self.sample_inference_content = settings.sample_inference_content
        self.historically_high_inferenced_models = (
            settings.historically_high_inferenced_models
        )

    def load(self) -> None:
        """Initializes the OnclusiveApiClient and sets the model state to ready."""
        self.model = OnclusiveApiClient
        self.ready = True

    def are_all_models_live(self) -> bool:
        """Check the liveness of all models by sending a test request to each model's endpoint.

        Returns:
            bool: True if all models are live and responsive, False otherwise.
        """
        all_models_live = True
        for model_id in AVAILABLE_MODELS.keys():
            if not self._should_check_model(model_id):
                continue
            client = self._create_client(model_id)
            current_model = self._get_current_model(client, model_id)
            try:
                response_schema = current_model(
                    client, content=settings.sample_inference_content
                )
                if response_schema.attributes.iptc is None:
                    logger.error(
                        f"Error while inferencing the IPTC model {model_id}: empty attributes"
                    )
                    self.last_failed[model_id] = True
                    all_models_live = False
                    break
            except Exception as e:
                logger.error(
                    f"Error while inferencing the IPTC model {model_id}: {str(e)}"
                )
                self.last_failed[model_id] = True
                all_models_live = False
                break
        return all_models_live

    def _calculate_probability_with_decay(self, model_id: str) -> float:
        """Calculate the probability of checking a model based on its historical inference frequency.

        The probability decays over time, incentivizing less frequent checks if the model
        has not been checked recently.

        Args:
            model_id (str): The unique identifier of the model.

        Returns:
            float: A probability value that decreases as more time elapses since the last check.
        """
        now = time.time()
        if self.last_checked.get(model_id) is None:
            self.last_checked[model_id] = now
        last_time = self.last_checked.get(model_id, now)
        elapsed = now - last_time
        base_probability = (
            0.3 if model_id in settings.historically_high_inferenced_models else 0.1
        )
        time_factor = min(1, elapsed / 3600)
        decayed_probability = min(
            1, base_probability + (1 - base_probability) * time_factor
        )

        return decayed_probability

    def _should_check_model(self, model_id: str) -> bool:
        """Determine whether to check the model based on a probabilistic decision influenced by time decay.

        Args:
            model_id (str): The unique identifier of the model.

        Returns:
            bool: True if the model should be checked based on the current probability influenced by
            historical frequency and time decay; False otherwise.
        """
        if self.last_failed.get(model_id):
            self.last_failed[model_id] = None
            return True
        probability = self._calculate_probability_with_decay(model_id)
        should_check = random.random() < probability
        if should_check:
            self.last_checked[model_id] = time.time()
        return should_check

    def _get_model_id_from_label(self, label: str) -> str:
        """Retrieve the model ID corresponding to a given label.

        Args:
            label (str): The label for which to find the corresponding model ID.

        Returns:
            str: The corresponding model ID or an empty string if the label is not found.

        Raises:
            ValueError: If the label does not exist in the dictionary.
        """
        if settings.test_model_sequence:
            return settings.test_model_sequence.pop(0)

        if label in TOPIC_TO_ID:
            return TOPIC_TO_ID[label]
        else:
            raise ValueError(f"No model ID found for label: {label}")

    def _endpoint(self, model_id: str) -> str:
        """Generates the endpoint URL for a given model ID using the configured template.

        Args:
            model_id (str): Model ID.

        Returns:
            str: Endpoint URL.
        """
        return settings.model_endpoint_template.format(model_id)

    def _create_client(self, model_id: str) -> OnclusiveApiClient:
        """Creates an API client for a given model identifier.

        Args:
            model_id (str): The identifier of the model for which the client will be created.

        Returns:
            OnclusiveApiClient: A client configured to interact with the specified model.
        """
        return self.model(
            host=self._endpoint(model_id),
            api_key=settings.model_endpoint_api_key,
            secure=settings.model_endpoint_secure,
        )

    def _get_current_model(
        self, model_client: OnclusiveApiClient, model_id: str
    ) -> Any:
        """Retrieves a model-specific method from the API client based on the model ID.

        Args:
            model_client (OnclusiveApiClient): The API client instance.
            model_id (str): The identifier of the model.

        Returns:
            Any: The callable API method associated with the given model ID.
        """
        return getattr(model_client, f"iptc_{model_id}")

    def _invoke_model(
        self, model_client: OnclusiveApiClient, model_id: str, content: str
    ) -> PredictResponseSchema:
        """Invokes the API call for the specified model with the provided content.

        Args:
            model_client (OnclusiveApiClient): The API client instance.
            model_id (str): The identifier of the model.
            content (str): The content to be processed by the model.

        Returns:
            PredictResponseSchema: The response from the model after processing the input content.
        """
        current_model = self._get_current_model(model_client, model_id)
        return current_model(model_client, content=content)

    def _get_current_class_dict(self, current_index: int) -> Dict[str, Dict]:
        """Determines which class dictionary should be used based on the current index in the process.

        Args:
            current_index (int): The index that determines which class dictionary to use.

        Returns:
            Dict[str, Dict]: The class dictionary appropriate for the current index.
        """
        if current_index == 0:
            return CLASS_DICT_SECOND
        elif current_index == 1:
            return CLASS_DICT_THIRD
        else:
            return {}

    def _get_combined_prediction(
        self, content: str, levels: List[str], current_index: int = 0
    ) -> Dict[str, float]:
        """Recursively combines predictions from different levels.

        Args:
            content (str): The content to be analyzed.
            levels (List[str]): A list of model identifiers that define the hierarchy of
            predictions.
            current_index (int, optional): The current index in the levels list to process.
            Defaults to 0.

        Returns:
            Dict[str, float]: A dictionary with combined labels as keys and their aggregated
            scores as values.

        Raises:
            Exception: Propagates any exceptions raised during API calls.
        """
        combined_prediction: Dict[str, float] = {}
        if current_index >= len(levels):
            return combined_prediction

        current_label = levels[current_index]
        model_id = self._get_model_id_from_label(current_label)
        client = self._create_client(model_id)

        try:
            prediction_response = self._invoke_model(client, model_id, content)
            processed_prediction = self._process_prediction_response(
                prediction_response
            )
            filtered_prediction = self._filter_prediction(processed_prediction)

            for label, score in filtered_prediction.items():
                combined_label = " > ".join(
                    levels[1 : current_index + 1] + [label]  # noqa: E203
                )
                combined_score = combined_prediction.get(combined_label, 1) * score
                combined_prediction[combined_label] = combined_score

                class_dict = self._get_current_class_dict(current_index)

                if label in class_dict and label not in levels:
                    deeper_levels = levels + [label]
                    deeper_predictions = self._get_combined_prediction(
                        content, deeper_levels, current_index + 1
                    )
                    for deeper_label, deeper_score in deeper_predictions.items():
                        combined_prediction[deeper_label] = (
                            deeper_score * combined_score
                        )

        except Exception as e:
            logger.error(f"Error with Topic API: {e}")
            raise

        return combined_prediction

    def _process_prediction_response(
        self, prediction_response: PredictResponseSchema
    ) -> Dict[str, float]:
        """Processes the raw prediction response to extract and transform IPTC data.

        Args:
            prediction_response (PredictResponseSchema)

        Returns:
            Dict[str, float]: A dictionary with IPTC labels as keys and their scores
            as values, sorted by scores in descending order.
        """
        iptc_dict = {
            item.label: item.score for item in prediction_response.attributes.iptc
        }
        if "medicine" in iptc_dict:
            iptc_dict["preventative medicine"] = iptc_dict.pop("medicine")
        return dict(sorted(iptc_dict.items(), key=lambda x: x[1], reverse=True))

    def _filter_prediction(self, prediction: Dict[str, float]) -> Dict[str, float]:
        """Filters predictions based on a dynamic cutoff.

        Args:
            prediction (Dict[str, float]): A dictionary of predictions with scores.

        Returns:
            Dict[str, float]: A dictionary containing only the predictions that have a score
                            above the calculated cutoff.
        """
        cutoff = 1 / len(prediction) if prediction else 0
        return {p: score for p, score in prediction.items() if score > cutoff}

    def _process_combined_predictions(
        self, prediction: Dict[str, float]
    ) -> Dict[str, float]:
        """Processes and filters predictions based on a minimum score cutoff.

        Args:
            prediction (Dict[str, float]): The combined predictions to be processed.

        Returns:
            Dict[str, float]: A dictionary of the top predictions sorted by score
            in descending order.
        """
        filtered_predictions = {
            p: round(score, 3)
            for p, score in prediction.items()
            if score > settings.min_score_cutoff
        }
        return dict(
            sorted(filtered_predictions.items(), key=lambda x: x[1], reverse=True)[
                : settings.max_topic_num
            ]
        )

    def _postprocess_predictions(
        self, predictions: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Processes prediction data to extract and transform into a list of dictionary items.

        Args:
            predictions (Dict[str, float]): A dictionary with topics as keys and scores as values.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing 'label', 'score',
                                and 'mediatopic_id' for each processed topic.

        Note:
            This function excludes topics listed in DROP_LIST and translates topics using
            CONVERSION_DICT before looking up their corresponding media topic IDs in TOPIC_TO_ID.
        """
        processed = []

        for topic, score in predictions.items():

            specific_topic: str = topic.split(">")[-1].strip()

            if specific_topic in DROP_LIST:
                continue

            converted_specific_topic = CONVERSION_DICT.get(
                specific_topic, specific_topic
            )

            mediatopic_id: str = TOPIC_TO_ID.get(
                converted_specific_topic, TOPIC_TO_ID.get(specific_topic)
            )

            if specific_topic != converted_specific_topic:
                topic = re.sub(r"(?<=> )[^>]*$", converted_specific_topic, topic)

            processed.append(
                {"label": topic, "score": score, "mediatopic_id": mediatopic_id}
            )

        return processed

    @filter_language(
        supported_languages=settings.supported_languages,
        raise_if_none=True,
    )
    def _predict(
        self, content: str, language: str, levels: List[str], current_index: int = 0
    ) -> List[Dict[str, Any]]:
        """Aggregated prediction method that filters unsupported languages.

        Args:
            content (str): The content to be analyzed.
            language (str): The language of the text.
            levels (List[str]): A list of model identifiers that define the hierarchy of
            predictions.
            current_index (int, optional): The current index in the levels list to process.
            Defaults to 0.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing 'label', 'score',
                                and 'mediatopic_id' for each processed topic.
        """
        combined_prediction = self._get_combined_prediction(
            content=content, levels=levels
        )
        processed_predictions = self._process_combined_predictions(combined_prediction)
        iptc_topics = self._postprocess_predictions(processed_predictions)
        return iptc_topics

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Topic Multi-model prediction based on dynamic response labels.

        Args:
            payload (PredictRequestSchema): Prediction request payload.
        """
        inputs = payload.attributes
        parameters = payload.parameters
        # Execute predictions in a language-aware context
        try:
            iptc_topics = self._predict(
                content=inputs.content, language=parameters.language, levels=["root"]
            )
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=204, detail=language_exception.message
            )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"iptc_topic": iptc_topics},
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served IPTC Multi model.

        Returns:
            BioResponseSchema: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )
