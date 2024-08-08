"""Queries."""
# isort: skip_file

# from abc import abstractmethod
from typing import Dict, Optional, Union

# 3rd party libraries
import ast
import json
import requests
from pydantic import SecretStr, Field

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel, OnclusiveBaseSettings
from onclusiveml.queries.exceptions import (
    QueryESException,
    QueryPostException,
    QueryGetException,
    QueryDeleteException,
    QueryMissingIdException,
    QueryIdException,
)


class MediaAPISettings(OnclusiveBaseSettings):
    """Media API Settings."""

    media_client_id: SecretStr = Field(
        default="...",
        exclude=True,
    )
    media_client_secret: SecretStr = Field(
        default="...",
        exclude=True,
    )
    media_username: SecretStr = Field(
        default="...",
        exclude=True,
    )
    media_password: SecretStr = Field(
        default="...",
        exclude=True,
    )

    GRANT_TYPE: str = "client_credentials"
    SCOPE: str = "c68b92d0-445f-4db0-8769-6d4ac5a4dbd8/.default"
    AUTHENTICATION_URL: str = "https://login.microsoftonline.com/a4002d19-e8b4-4e6e-a00a-95d99cc7ef9a/oauth2/v2.0/token"  # noqa: E501
    PRODUCTION_TOOL_ENDPOINT: str = (
        "https://staging-querytool-api.platform.onclusive.org"
    )
    MEDIA_API_URL: str = "https://crawler-api-prod.airpr.com/v1"


class BaseQueryProfile(OnclusiveBaseModel):
    """Base boolean query profile."""

    def headers(self, settings: MediaAPISettings) -> Dict:
        """Media API request headers."""
        return {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token(settings)}",
        }

    def _token(self, settings: MediaAPISettings) -> Optional[str]:
        settings_dict = settings.model_dump()
        settings_dict["client_secret"] = settings.media_client_secret.get_secret_value()
        settings_dict["client_id"] = settings.media_client_id.get_secret_value()
        settings_dict["grant_type"] = settings.GRANT_TYPE
        settings_dict["scope"] = settings.SCOPE

        token_request = requests.post(settings.AUTHENTICATION_URL, settings_dict)
        return token_request.json().get("access_token")

    def es_query(self, settings: MediaAPISettings) -> Union[Dict, None]:
        """Elastic search query."""
        # call the media to translate Boolean query -> ES query
        response = self._from_boolean_to_media_api(settings)
        if response:
            data = response.get("query", {})
            return {"bool": data["es_query"]}
        else:
            raise QueryESException()

    def _from_boolean_to_media_api(
        self, settings: MediaAPISettings
    ) -> Union[Dict, None]:
        """Translates a boolean query in media API format."""
        json_data = {
            "name": "ml-query",
            "description": "used by ML team to translate queries from boolean to media API",
            "booleanQuery": self.query,
        }
        # add query to database
        post_res = requests.post(
            f"{settings.PRODUCTION_TOOL_ENDPOINT}/v1/topics/",
            headers=self.headers(settings),
            json=json_data,
        )
        if post_res.status_code == 201:
            post_res = post_res.json()
            query_id = post_res.get("id")

            # check if id is given after inserting boolean query into database
            if query_id is None:
                raise QueryMissingIdException(boolean_query=self.query)

            # retrieve query from database
            get_res = requests.get(
                f"{settings.PRODUCTION_TOOL_ENDPOINT}/v1/mediaContent/translate/mediaapi?queryId={query_id}",  # noqa: E501
                headers=self.headers(settings),
            )
            if get_res.status_code == 200:
                # delete query from database
                del_res = requests.delete(
                    f"{settings.PRODUCTION_TOOL_ENDPOINT}/v1/topics/{query_id}",  # noqa: E501
                    headers=self.headers(settings),
                )
                if del_res.status_code != 204:
                    raise QueryDeleteException(
                        boolean_query=self.query, query_id=query_id
                    )
                return get_res.json()
            else:
                raise QueryGetException(boolean_query=self.query, query_id=query_id)
        else:
            raise QueryPostException(boolean_query=self.query)


class StringQueryProfile(BaseQueryProfile):
    """Prod tools query."""

    string_query: str

    @property
    def query(self) -> str:
        """String query."""
        # api call to query tool
        return self.string_query


class ProductionToolsQueryProfile(BaseQueryProfile):
    """Query ID to Boolean."""

    version: int
    query_id: str
    settings: MediaAPISettings = MediaAPISettings()

    @property
    def query(self) -> Union[str, None]:
        """Translate query id to string query."""
        request_result = requests.get(
            f"{self.settings.PRODUCTION_TOOL_ENDPOINT}/v{self.version}/topics/{self.query_id}",
            headers=self.headers(self.settings),
        )
        if request_result.status_code == 200:
            return request_result.json().get("booleanQuery")
        else:
            raise QueryIdException(query_id=self.query_id)


class MediaApiStringQuery(BaseQueryProfile):
    """360 Media Api query to es query."""

    string_query: str

    @property
    def media_query(self) -> str:
        """Media Api String query."""
        # api call to query tool
        json_query = ast.literal_eval(self.string_query)
        return json_query

    def run(
        self,
        settings: MediaAPISettings,
        page: int = 1,
        limit: int = 25,
        only_id: bool = True,
    ) -> Union[Dict, None]:
        """Runs a media API query to generate es query."""
        query = self.media_query
        query["page"] = page
        query["limit"] = limit
        query["sort"] = ["_score"]
        query["show_query"] = True

        MEDIA_API_BASE_URL = settings.MEDIA_API_URL
        username = settings.media_username.get_secret_value()
        password = settings.media_password.get_secret_value()

        if only_id:
            query["return_fields"] = ["id", "url", "content"]
        res = requests.post(
            f"{MEDIA_API_BASE_URL}/search/articles",
            json=query,
            auth=(username, password),
        )
        json_res = res.json()
        final_res = json.loads(json_res["es_query"])["query"]
        return final_res

    def es_query(self, settings: MediaAPISettings) -> Union[Dict, None]:
        """Elastic search query."""
        # call the media to translate Boolean query -> ES query
        response = self.run(settings)
        if response:
            return response
        else:
            raise QueryESException()
