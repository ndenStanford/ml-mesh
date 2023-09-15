"""Conftest."""

# Standard Library
import json

# 3rd party libraries
import pytest
from requests_toolbelt.sessions import BaseUrlSession

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.server_models import BioResponseModel, PredictResponseModel


# from typing import List


@pytest.fixture
def test_client():
    """Client-like session with base url to avoid duplication.

    References:
        https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession
    """
    serving_params = ServingParams()
    model_server_port = serving_params.uvicorn_settings.http_port
    test_model_server_url = f"http://serve:{model_server_port}"

    return BaseUrlSession(base_url=test_model_server_url)


@pytest.fixture
def test_model_name() -> str:
    """Model name fixture."""
    return "topic-detection"


@pytest.fixture
def test_inference_params(test_served_model_artifacts):
    """Test loading inference parameters."""
    with open(test_served_model_artifacts.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predict_input() -> str:
    """Test predict input."""
    return "Call functions to detect topic for articles"


@pytest.fixture
def test_expected_predict_output() -> Dict[str, str]:
    """Predicted response model fixture."""
    return PredictResponseModel(
        topic={
            "Risk detection": "Risk detection in the science and technology industry primarily pertains to the unpredictability and volatility of weather patterns, influenced by factors like climate change and global warming. This calls for advanced climate modeling and thorough interpretation of weather impacts for accurate risk anticipation and mitigation. Moreover, the sector's limited understanding of universal anomalies, including black holes, pose additional risks, emphasizing the need for improved cosmic investigation and decoding of extraterrestrial objects like Martian meteorites.",  # noqa:E501
            "Opportunities": "The science and technology industry holds vast potential in addressing climate change and health sector challenges. There are opportunities to develop technologies to manage and mitigate climate impacts like reducing carbon emissions and foreseeing volatile weather patterns. In the health sector, advancements in immunization technology, such as CodaVax-RSV and Moderna's ARNm-1273.214, suggest potential growth in vaccine development. The field of neuroscience and bio-communication, specifically studies in neurotransmitter activities and reflex system dynamics, also present untapped opportunities.",  # noqa:E501
            "Threats for the brand": "Apologies, but it's impossible to summarize or combine the main points as there's no summaries mentioned related to the science and technology industry and the threats for the brand. Please provide relevant summaries for further assistance.",  # noqa:E501
            "Company or spokespersons": "In the science and technology industry, key spokespersons are highlighting significant advancements and challenges. Virginia Tech's Craig Ramseyer emphasizes the need for carbon emission reduction strategies due to climate change impacts. Meanwhile, companies such as Codagenix and Moderna are making breakthroughs in the medical field. Codagenix's CodaVax-RSV drug received FDA approval, with CEO J. Robert Coleman underscoring the vaccine's efficacy. Moderna's CEO Stéphane Bancel announced favorable clinical trial results of their COVID-19 booster vaccine, mRNA-1273.214, highlighting the benefits of their bivalent booster approach in combating virus variants.",  # noqa:E501
            "Brand Reputation": "Apologies for the confusion, but you didn't provide any summaries related to the science and technology industry focusing on the category of Brand Reputation. Could you please provide the required summaries for me to combine and create a concise summary?",  # noqa:E501
            "CEO Reputation": "Apologies for the confusion, but there aren't any summaries provided to combine and create a concise summary about the reputation of CEOs within the science and technology industry. Please provide the relevant summaries.",  # noqa:E501
            "Customer Response": "As no summaries have been provided, a combined summary cannot be produced. Please provide summaries from articles related to the science and technology industry, specifically focusing on the category of Customer Response.",  # noqa:E501
            "Stock Price Impact": "As no summaries are provided, a combined summary cannot be generated. Please provide relevant summaries related to 'stock price impact' in the 'science and technology' industry.",  # noqa:E501
            "Industry trends": "The science and technology industry is currently marked by two major trends. Firstly, there is a growing focus on understanding weather patterns and climate changes. Research emphasizes the potential threats of rising global temperatures, leading to the development of technologies aimed at climate change mitigation. Secondly, significant advancements are being made in vaccine research and development, with companies like Codagenix and Moderna demonstrating progress. The industry trend is moving towards creating effective vaccines for prevalent diseases, including ongoing health crises like the Covid-19 pandemic, showcasing an increase in healthcare technology.",  # noqa: E501
        }  # noqa: E501
    )  # noqa:E501


@pytest.fixture
def test_expected_bio_output(test_model_name):
    """Test bio output."""
    return BioResponseModel(model_name=test_model_name)
