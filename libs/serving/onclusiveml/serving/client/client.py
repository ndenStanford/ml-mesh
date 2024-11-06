"""ML APIs client."""

# Standard Library
from typing import Any

# Internal libraries
import onclusiveml.serving.serialization.entity_linking.v1 as entity_linking_v1
import onclusiveml.serving.serialization.gch_summarization.v1 as gch_summarization_v1
import onclusiveml.serving.serialization.iptc.v1 as iptc_v1
import onclusiveml.serving.serialization.iptc_multi.v1 as iptc_multi_v1
import onclusiveml.serving.serialization.lsh.v1 as lsh_v1
import onclusiveml.serving.serialization.ner.v1 as ner_v1
import onclusiveml.serving.serialization.sentiment.v1 as sentiment_v1
import onclusiveml.serving.serialization.topic.v1 as topic_v1
import onclusiveml.serving.serialization.topic_summarization.v1 as topic_summarization_v1
import onclusiveml.serving.serialization.translation.v1 as translation_v1
from onclusiveml.serving.client._bind import bind


class OnclusiveApiClient:
    """Onclusive Api client.

    Attributes:
        host (str): client hostname
        api_key (str): client api key.
        api_key_header (str): client api key header key.
        secure (bool): if yes, request is made through a secure endpoint.

    Example:
        >>> from onclusiveml.serving.client import OnclusiveApiClient
        >>> client = OnclusiveApiClient(host="internal.api.ml.stage.onclusive.com", api_key="")
        >>> output = client.ner(content="text to extract from")
    """

    def __init__(
        self,
        host: str,
        api_key: str,
        api_key_header: str = "x-api-key",
        secure: bool = True,
    ) -> None:
        self.protocol = "https" if secure else "http"
        self.host = host
        self.api_key_header = api_key_header
        self.api_key = api_key
        # Created from onclusiveml.models.iptc.class_dict.AVAILABLE_MODELS
        # to avoid models lib dependencies from serving
        self.available_iptc_models = [
            "00000000",
            "01000000",
            "16000000",
            "02000000",
            "03000000",
            "04000000",
            "05000000",
            "06000000",
            "07000000",
            "09000000",
            "10000000",
            "11000000",
            "12000000",
            "13000000",
            "14000000",
            "15000000",
            "17000000",
            "20000209",
            "20000170",
            "20000385",
            "20000148",
            "20000139",
            "20000717",
            "20000756",
            "20000742",
            "20000735",
            "20000106",
            "20000129",
            "20000121",
            "20000082",
            "20000464",
            "20000446",
            "20000493",
            "20000538",
            "20000565",
            "20000056",
            "20000065",
            "20000053",
            "20000822",
            "20000002",
            "20000038",
            "20000045",
            "20000430",
            "20000424",
            "20000441",
            "20000657",
            "20000705",
            "20000697",
            "20000593",
            "20000574",
            "20000638",
            "20000621",
            "20000587",
            "20000649",
            "20000780",
            "20000808",
            "20000802",
            "20000775",
            "20000799",
            "20000788",
            "20000763",
        ]
        self.setup_iptc_bindings()

    def setup_iptc_bindings(self) -> None:
        """Dynamically create bindings for each model."""
        for model_id in self.available_iptc_models:
            namespace = f"iptc-{model_id}"
            setattr(
                self,
                f"iptc_{model_id}",
                bind(
                    namespace=namespace,
                    version=1,
                    method="POST",
                    endpoint="predict",
                    request_attributes_schema=iptc_v1.PredictRequestAttributeSchemaV1,
                    request_parameters_schema=iptc_v1.PredictRequestParametersSchemaV1,
                    response_attributes_schema=iptc_v1.PredictResponseAttributeSchemaV1,
                ),
            )

    ner = bind(
        namespace="ner",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=ner_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=ner_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=ner_v1.PredictResponseAttributeSchemaV1,
    )

    entity_linking = bind(
        namespace="entity-linking",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=entity_linking_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=entity_linking_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=entity_linking_v1.PredictResponseAttributeSchemaV1,
    )

    topic_summarization = bind(
        namespace="topic-summarization",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=topic_summarization_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=topic_summarization_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=topic_summarization_v1.PredictResponseAttributeSchemaV1,
    )

    topic = bind(
        namespace="topic",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=topic_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=topic_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=topic_v1.PredictResponseAttributeSchemaV1,
    )

    gch_summarization = bind(
        namespace="gch-summarization",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=gch_summarization_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=gch_summarization_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=gch_summarization_v1.PredictResponseAttributeSchemaV1,
    )

    sentiment = bind(
        namespace="sentiment",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=sentiment_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=sentiment_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=sentiment_v1.PredictResponseAttributeSchemaV1,
    )

    lsh = bind(
        namespace="lsh",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=lsh_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=lsh_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=lsh_v1.PredictResponseAttributeSchemaV1,
    )

    translation = bind(
        namespace="translation",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=translation_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=translation_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=translation_v1.PredictResponseAttributeSchemaV1,
    )

    iptc_multi = bind(
        namespace="iptc-multi",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=iptc_multi_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=iptc_multi_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=iptc_multi_v1.PredictResponseAttributeSchemaV1,
    )

    def __getitem__(self, model: str) -> Any:
        """Dictionary like behaviour to access specific API."""
        model = model.replace("-", "_")
        model_attr = getattr(self, model)
        return model_attr
