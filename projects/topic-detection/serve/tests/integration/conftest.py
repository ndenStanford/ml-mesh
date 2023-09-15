"""Conftest."""

# Standard Library
from typing import Dict

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Source
from src.serve.model_server import get_model_server
from src.serve.server_models import (
    BioResponseModel,
    PredictInputDocumentModel,
    PredictResponseModel,
)


@pytest.fixture
def test_client():
    """Client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
    # return "Call functions to generate hash signatures for each article"
    return PredictInputDocumentModel(
        industry="Science and technology",
        content=[
            """
            India's semiconductor component market will see its cumulative revenues climb to $300 billion during 2021-2026,
            a report said Tuesday. The ‘India Semiconductor Market Report, 2019-2026',
            a joint research by the India Electronics & Semiconductor Association (IESA) and Counterpoint Research,
            observed that India is poised to be the second largest market in the world in terms of scale and growing demand for
            semiconductor components across several industries and applications.
            It added that this was being bolstered by the increasing pace of digital transformation and the adoption of
            new technologies and covers smartphones, PCs, wearables, cloud data centers,
            Industry 4.0 applications, IoT, smart mobility, and advanced telecom and public utility infrastructure.
            “While the country is becoming one of the largest consumers of electronic and semiconductor components,
            most components are imported, offering limited economic opportunities for the country.
            Currently, only 9% of this semiconductor requirement is met locally,” the report said.
            it noted that India's end equipment market in 2021 stood at $119 billion in terms of revenue and
            is expected to grow at a CAGR of 19% from 2021 to 2026.
            It said that the Electronic System Design and Manufacturing (ESDM) sector in India will play a major role in the
            country's overall growth, from sourcing components to design manufacturing.
            “Before the end of this decade, there will be nothing that will not be touched by electronics and the ubiquitous ‘chip,
            '” IESA CEO Krishna Moorthy said. “Be it fighting carbon emissions, renewable energy, food safety, or healthcare,
            the semiconductor chip will be all-pervasive.”
            Counterpoint Research vice president Neil Shah added that consumption will not only come from the advanced
            semiconductor-heavy 5G and fiber-to-the-home (FTTH) network infrastructure equipment,
            which will contribute to more than 14% of the total semiconductor consumption in 2026,
            but also from the highly capable AI-driven 5G endpoints,
            from smartphones, tablets, PCs, connected cars, industrial robotics to private networks.
            “The telecom sector with the advent of 5G and fiber network rollout will be a key catalyst in boosting
            the semiconductor components consumption,” Shah said.
            “Also, ongoing efforts to embrace cleaner and greener vehicles (electric vehicles) will provide an impetus for
            the automobile industry to adopt advanced technologies,
            which in turn will boost the demand for semiconductor components in India.”
            He also believed that consumer electronics, industrial, and mobile and wearables will be the other key industries
            for the growth of the semiconductor market in India.
            Further, this semiconductor demand will not only be driven by domestic consumption but also by the growing share of exports.
            Mobile and wearables,
            IT and industrial sectors alone contributed to almost 80% of the semiconductor revenues in India in 2021, the research found.
            Tarun Pathak, research director at Counterpoint Research, said the gradual shift from feature phones to smartphones
            has been generating increased proportions of advanced logic processors, memory, integrated controllers, sensors and
            other components. “This will continue to drive the value of the semiconductor content in smartphones, which is still an
            under-penetrated segment in India, aided by the rise of wearables such as smartwatch and TWS,” he said.""",  # noqa: E501
        ],
    )


@pytest.fixture
def test_expected_predict_output() -> Dict[str, str]:
    """Expected predict output fixture."""
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
    )


@pytest.fixture
def test_expected_bio_output():
    """Test expected bio output."""
    return BioResponseModel(model_name="topic-detection")
