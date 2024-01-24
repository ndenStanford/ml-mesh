"""Transforms."""

# Standard Library
from typing import Any, Dict, Generator, List, Optional, Tuple

# 3rd party libraries
from apache_beam import DoFn, ParDo, PCollection, PTransform
from pydantic import SecretStr

# Internal libraries
from onclusiveml.data.beam.exceptions import BeamPipelineException
from onclusiveml.serving.client import OnclusiveApiClient


class _OnclusiveApiCall(DoFn):
    """Internal ``DoFn`` to make a call to a ML API."""

    def __init__(
        self,
        host: str,
        api_key: SecretStr,
        secure: bool,
        namespace: str,
        version: int,
        in_keys: List[str],
        out_key: Optional[str] = None,
        **kwargs: Dict
    ):
        super(_OnclusiveApiCall, self).__init__()
        self.host = host
        self.api_key = api_key
        self.in_keys = in_keys
        self._out_key = out_key
        self.secure = secure
        self.namespace = namespace
        self._client = None
        self._parameters = kwargs
        self.version = version

    @property
    def client(self) -> OnclusiveApiClient:
        """API client instance."""
        return self._client

    @property
    def parameters(self) -> Dict:
        """API call parameters."""
        return self._parameters

    @property
    def out_key(self) -> str:
        return self._out_key if self._out_key is not None else self.namespace

    def start_bundle(self) -> None:
        """Start Bundle."""
        self._client = OnclusiveApiClient(
            host=self.host,
            api_key=self.api_key.get_secret_value(),
            secure=self.secure,
        )

    def finish_bundle(self) -> None:
        """Finish Bundle."""
        self._client = None

    def _retrieve(self, contents: Dict[str, Any], key: str) -> Dict:
        nested_keys = key.split(".")
        retrieved_contents: Any = contents.get(nested_keys[0])
        for key_ in nested_keys[1:]:
            retrieved_contents = retrieved_contents.get(key_)
        return retrieved_contents

    def _extract_input(self, contents: Dict, keys: List[str]) -> Dict:
        """Retrive input data from element."""
        return {out_key: self._retrieve(contents, out_key) for out_key in keys}

    def _predict(self, element: Tuple) -> Tuple:
        """API call to predict enriched features."""
        key, contents = element
        response = self.client[self.namespace](
            **self._extract_input(contents, self.in_keys), **self.parameters
        )
        contents[self.out_key] = response.data.attributes.dict()
        return key, contents

    def process(self, element: Tuple) -> Generator[Tuple, None, None]:
        """Process transform."""
        # get request schema instance from element
        try:
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print(self._predict(element))
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            print("*" * 128)
            yield self._predict(element)
        except Exception:
            raise BeamPipelineException()


class MachineLearningEnrichment(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for ML enrichment of documents.

    Args:
        host (str): client hostname
        api_key (str): client api key.
        secure (bool): if yes, request is made through a secure endpoint.
        namespace (str): api project name
        version (int): api version
        keys (List[str]): input keys from source data

    Examples:
            with beam.Pipeline(options=PipelineOptions()) as p:
        _ = (
            p
            | "Read From Kafka"
            >> KafkaConsume(
                consumer_config={"topic": "notifications",
                               "bootstrap_servers": "localhost:9092",
                               "group_id": "notification_consumer_group"},
                topics=["beam.input"],
            )
            | "Decode" >> beam.Map(lambda x: (x[0], json.loads(x[1])))
            | "Enrichment "
            >> MachineLearningEnrichment(
                host="internal.api.ml.prod.onclusive.com",
                secure=True,
                keys=[
                    "content",
                    "language",
                ]
                api_key="",
                namespace="ner",
                version=1,
            )
            | 'Writing to stdout' >> beam.Map(print)
    """

    def __init__(
        self,
        host: str,
        api_key: SecretStr,
        secure: bool,
        namespace: str,
        version: int,
        in_keys: List[str],
        out_key: Optional[str] = None,
        **kwargs: Dict
    ) -> None:
        super(MachineLearningEnrichment, self).__init__()
        self._attributes = dict(
            host=host,
            secure=secure,
            namespace=namespace,
            version=version,
            api_key=api_key,
            in_keys=in_keys,
            out_key=out_key,
            **kwargs
        )

    def expand(self, pcoll: PCollection) -> PCollection:
        """Apply transform to collection.

        Args:
            pcoll (PCollection): input collection.
        """
        return pcoll | ParDo(_OnclusiveApiCall(**self._attributes))
