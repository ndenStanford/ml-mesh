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


def invoke_el(content: str, url: str, api_key: SecretStr, lang: str = "en") -> Any:
    """Invokes the API and returns the respons.

    Args:
        content (str): Sentence with the eventual entity.
        url (str): endpoint of the API
        api_key (str): key of the URL
        lang (str): language.

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
            "parameters": {"lang": lang},
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def entity_linking(content: str, lang: str = "en") -> Optional[str]:
    """Returns the eventual wiki_link associated to a given entity.

    Args:
        content (str): Sentence with the eventual entity.
        lang (str): language.

    Returns:
        String of the wiki_link or None.
    """
    api_key = settings.entity_linking_stage.api_key
    url = settings.entity_linking_stage.url

    response = invoke_el(content, url, api_key, lang)

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
