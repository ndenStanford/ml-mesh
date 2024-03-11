"""Queries."""

# Standard Library
from abc import abstractmethod

# 3rd party libraries
import requests
from pydantic import SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSchema, OnclusiveFrozenSettings


class MediaAPISettings(OnclusiveFrozenSettings):
    """Media API Settings."""
    client_id: SecretStr
    client_secret: SecretStr
    grant_type: str = "client_credentials"
    scope: str


class BaseQueryProfile(OnclusiveBaseSchema):
    """Base boolean query profile."""

    ml_query_id: str = "6bcd99ee-df08-4a7e-ad5e-5cdab4b558c3"
    authentication_url: str = "https://login.microsoftonline.com/a4002d19-e8b4-4e6e-a00a-95d99cc7ef9a/oauth2/v2.0/token"


    def headers(self, settings: MediaAPISettings) -> Dict:
        """Media API request headers."""

        return {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._token(settings)}',
        }

    def _token(self, settings: MediaAPISettings) -> Optional[str]
        token_request = requests.post(
            self.authentication_url,
            settings.dict()
        )
        token_request.json().get("access_token")

    @property
    @abstractmethod
    def query(self) -> str:
        """String query."""

    def es_query(self, settings: MediaAPISettings) -> Dict:
        """Elastic search query."""
        # call the media to translate Boolean query -> ES query
        data = self._from_boolean_to_media_api(settings).get("query", {})
        return data["es_query"]

    def _from_boolean_to_media_api(self, settings: MediaAPISettings) -> Dict:
        """Translates a boolean query in media API format"""
        json_data = {
            'name': 'ml-query',
            'description': 'used by ML team to translate queries from boolean to media API',
            'booleanQuery': self.query,
        }
        _ = requests.put(f'{MEDIA_API_URI}/v1/topics/{self.ml_query_id}', headers=self.headers(settings), json=json_data)
        response = requests.get(f'{MEDIA_API_URI}/v1/mediaContent/translate/mediaapi?queryId={self.ml_query_id}', headers=self.headers(settings))
        return response.json()


class StringQueryProfile(BaseQueryProfile):
    """Prod tools query."""

    def __init__(self, string_query: str)
        self._string_query = string_query

    @property
    def query(self) -> str:
        """String query."""
        # api call to query tool
        return self.string_query



if __name__ == "__main__":
    settings = MediaAPISettings()

    query = StringQueryProfile("""("telecom*" OR "broadband*") NOT (("EEF" OR "EEFs" OR "EEF's")))""")

    es_query = query.es_query(settings)
