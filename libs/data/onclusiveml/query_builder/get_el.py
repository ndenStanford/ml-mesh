"""Entity Linkng."""

# Standard Library
import json
from typing import Any, Optional

# 3rd party libraries
import requests
from pydantic import SecretStr

# Internal libraries
from onclusiveml.query_builder.settings import get_settings


settings = get_settings()


def invoke_el(content: str, url: str, api_key: SecretStr, language: str = "en") -> Any:
    """Invokes the API and returns the respons.

    Args:
        content (str): Sentence with the eventual entity.
        url (str): endpoint of the API
        api_key (str): key of the URL
        language (str): language.

    Returns:
        response.
    """
    headers = {
        "content-type": "application/json",
        "x-api-key": api_key.get_secret_value(),
    }
    data = {
        "data": {
            "namespace": "entity-linking",
            "attributes": {"content": content},
            "parameters": {"lang": language},
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def predict_entity_linking(content: str, language: str = "en") -> Optional[str]:
    """Returns the eventual wiki_link associated to a given entity.

    Args:
        content (str): Sentence with the eventual entity.
        language (str): language.

    Returns:
        String of the wiki_link or None.
    """
    try:
        api_key = settings.entity_linking_prod.api_key

        url = settings.entity_linking_prod.predict_url

        response = invoke_el(content, url, api_key, language)

        if response.status_code == 200:
            result = response.json()
            wiki_link = (
                result.get("data", {})
                .get("attributes", {})
                .get("entities", [])[0]["wiki_link"]
            )
            return wiki_link
        else:
            print(f"Error with prod endpoint: {response.status_code}, {response.text}")
            return None

    except Exception as e:
        print(f"RequestException occurred: {e}")
        api_key = settings.entity_linking_stage.api_key

        url = settings.entity_linking_stage.predict_url

        response = invoke_el(content, url, api_key, language)

        if response.status_code == 200:
            result = response.json()
            wiki_link = (
                result.get("data", {})
                .get("attributes", {})
                .get("entities", [])[0]["wiki_link"]
            )
            return wiki_link
        else:
            print(f"Error with stage endpoint: {response.status_code}, {response.text}")
            return None
