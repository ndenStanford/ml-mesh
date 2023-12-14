"""NER."""

# Standard Library
import json
from typing import Any, List, Optional

# 3rd party libraries
import requests
from pydantic import SecretStr

# Internal libraries
from onclusiveml.query_builder.settings import get_settings


settings = get_settings()


def invoke_ner(content: str, url: str, api_key: SecretStr, lang: str = "en") -> Any:
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
            "namespace": "ner",
            "attributes": {"content": content},
            "parameters": {"language": lang},
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response


def predict_ner(
    content: str, candidates: List, lang: str = "en"
) -> List[Optional[str]]:
    """Returns the eventual list of entities in a sentence.

    Args:
        content (str): Sentence with the eventual entity.
        candidates (List): A list of the expected entities.
        lang (str): Language. Defaults to "en".

    Returns:
        List of string(s) of eventual entities or an empty list.
    """
    try:
        api_key = settings.NER_prod.api_key
        url = settings.NER_prod.predict_url

        response = invoke_ner(content, url, api_key, lang)

        if response.status_code == 200:
            result = response.json()
            entities = [
                entity["entity_text"]
                for entity in result.get("data", {})
                .get("attributes", {})
                .get("entities", [])
            ]
        else:
            print(f"Error: {response.status_code}, {response.text}")
            raise ValueError("Error in prod endpoint, switching to stage")

        result = [i for i in candidates if i in entities]
        return result

    except Exception as e:
        print(f"RequestException occurred: {e}")
        api_key = settings.NER_stage.api_key
        url = settings.NER_stage.predict_url

        response = invoke_ner(content, url, api_key, lang)

        if response.status_code == 200:
            result = response.json()
            entities = [
                entity["entity_text"]
                for entity in result.get("data", {})
                .get("attributes", {})
                .get("entities", [])
            ]
        else:
            print(f"Error with stage endpoint: {response.status_code}, {response.text}")
            raise ValueError("Error in stage endpoint")

        result = [i for i in candidates if i in entities]
        return result
