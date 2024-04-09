"""Queries."""
# isort: skip_file

# from abc import abstractmethod
from typing import Dict, Optional, Union

# 3rd party libraries
import requests
from pydantic import SecretStr, Field

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSchema, OnclusiveBaseSettings


class MediaAPISettings(OnclusiveBaseSettings):
    """Media API Settings."""

    client_id: SecretStr = Field(default="...", env="MEDIA_CLIENT_ID", exclude=True)
    client_secret: SecretStr = Field(
        default="...", env="MEDIA_CLIENT_SECRET", exclude=True
    )
    grant_type: str = "client_credentials"
    scope: str = "c68b92d0-445f-4db0-8769-6d4ac5a4dbd8/.default"
    ml_query_id: str = "6bcd99ee-df08-4a7e-ad5e-5cdab4b558c3"
    authentication_url: str = "https://login.microsoftonline.com/a4002d19-e8b4-4e6e-a00a-95d99cc7ef9a/oauth2/v2.0/token"  # noqa: E501
    media_api_url: str = "https://staging-querytool-api.platform.onclusive.org"

    def get_client_secret_value(self) -> str:
        """Get client_secret."""
        return self.client_secret.get_secret_value()

    def get_client_id_value(self) -> str:
        """Get client_id."""
        return self.client_id.get_secret_value()


class BaseQueryProfile(OnclusiveBaseSchema):
    """Base boolean query profile."""

    def headers(self, settings: MediaAPISettings) -> Dict:
        """Media API request headers."""
        return {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token(settings)}",
        }

    def _token(self, settings: MediaAPISettings) -> Optional[str]:
        settings_dict = settings.dict()
        settings_dict["client_secret"] = settings.client_secret.get_secret_value()
        settings_dict["client_id"] = settings.client_id.get_secret_value()
        settings_dict["grant_type"] = settings.grant_type
        settings_dict["scope"] = settings.scope

        token_request = requests.post(settings.authentication_url, settings_dict)
        return token_request.json().get("access_token")

    def es_query(self, settings: MediaAPISettings) -> Union[Dict, None]:
        """Elastic search query."""
        # call the media to translate Boolean query -> ES query
        response = self._from_boolean_to_media_api(settings)
        if response:
            data = response.get("query", {})
            return {"bool": data["es_query"]}
        return None

    def _from_boolean_to_media_api(
        self, settings: MediaAPISettings
    ) -> Union[Dict, None]:
        """Translates a boolean query in media API format."""
        json_data = {
            "name": "ml-query",
            "description": "used by ML team to translate queries from boolean to media API",
            "booleanQuery": self.query,
        }
        _ = requests.put(
            f"{settings.media_api_url}/v1/topics/{settings.ml_query_id}",
            headers=self.headers(settings),
            json=json_data,
        )
        if _.status_code == 204:
            response = requests.get(
                f"{settings.media_api_url}/v1/mediaContent/translate/mediaapi?queryId={settings.ml_query_id}",  # noqa: E501
                headers=self.headers(settings),
            )
            return response.json()

        return None


class StringQueryProfile(BaseQueryProfile):
    """Prod tools query."""

    string_query: str

    @property
    def query(self) -> str:
        """String query."""
        # api call to query tool
        return self.string_query
