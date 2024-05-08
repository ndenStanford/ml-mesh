"""Prediction model."""

# Standard Library
import re
from typing import Any, Dict, List, Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.iptc.class_dict import (
    CLASS_DICT_SECOND,
    CLASS_DICT_THIRD,
    CONVERSION_DICT,
    DROP_LIST,
    TOPIC_TO_ID,
)
from onclusiveml.serving.client import OnclusiveApiClient
from onclusiveml.serving.rest.serve import ServedModel

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

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="iptc-multi")

    def load(self) -> None:
        """Initializes the OnclusiveApiClient and sets the model state to ready."""
        self.model = OnclusiveApiClient
        self.ready = True

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
            api_key="",
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

        label = levels[current_index]
        model_id = self._get_model_id_from_label(label)
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
                        combined_prediction[deeper_label] = deeper_score

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

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Topic Multi-model prediction based on dynamic response labels.

        Args:
            payload (PredictRequestSchema): Prediction request payload.
        """
        inputs = payload.attributes

        combined_prediction = self._get_combined_prediction(inputs.content, ["root"])
        processed_predictions = self._process_combined_predictions(combined_prediction)
        iptc_topics = self._postprocess_predictions(processed_predictions)

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
