"""Conftest."""

# Standard Library
from typing import Dict

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.model_server import get_model_server
from src.serve.schema import BioResponseSchema


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_inference_params() -> str:
    """Predict parameter fixture."""
    return {}


@pytest.fixture
def test_client():
    """Client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
    return [
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
    ]


@pytest.fixture
def test_expected_predict_output() -> Dict[str, str]:
    """Expected predict output fixture. Temporarily unused bc GPT responses drift within 30mins."""
    return {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "topic-summarization",
            "attributes": {
                "topic": {
                    "Opportunities": "The science and technology industry has several opportunities for growth and development. Firstly, there is an increasing demand for semiconductor components in India, with the country projected to become the second largest market globally. Secondly, the expansion of the electronic system design and manufacturing sector will be crucial in meeting the demand for semiconductor components. Lastly, the adoption of advanced technologies in key industries such as consumer electronics and wearables will drive the demand for semiconductor components. Overall, these opportunities present a chance for the science and technology industry to drive growth, innovation, and economic development.",  # noqa: E501
                    "Risk detection": "Risk detection in the science and technology industry is crucial for ensuring safety and minimizing potential harm. Multiple articles emphasize the importance of effective risk detection strategies. These strategies involve the use of advanced technologies and analytical tools to identify and mitigate risks effectively. Key areas of focus include cybersecurity, data privacy, and emerging technologies. By implementing robust risk detection measures, organizations can safeguard their operations, protect sensitive information, and prevent potential threats. A proactive approach to risk detection is necessary to stay ahead in this rapidly evolving industry.",  # noqa: E501
                    "Threats for the brand": "The Science and Technology industry faces various threats to its brand. These threats encompass issues such as cybersecurity breaches, intellectual property theft, and reputational damage. Cyber attacks are a significant concern, with hackers targeting sensitive data and research. Intellectual property theft poses a risk as competitors may steal innovative ideas or technologies. Additionally, reputational damage can occur through negative publicity or unethical practices. It is crucial for companies in this industry to prioritize cybersecurity measures, protect intellectual property, and maintain a strong brand image to mitigate these threats.",  # noqa: E501
                    "Company or spokespersons": "In the field of science and technology, the focus is on companies and spokespersons. Various articles highlight key points in this industry. One article discusses the importance of having strong spokespersons who can effectively communicate complex scientific concepts to the public. Another article emphasizes the need for companies to have a clear vision and mission, supported by innovative products and services. Additionally, a different article explores the role of companies in driving advancements in technology and contributing to scientific research. Overall, this industry relies on companies and spokespersons to drive innovation, communicate scientific knowledge, and contribute to technological advancements.",  # noqa: E501
                    "Brand Reputation": "The target industry is Science and Technology, and the focus is on Brand Reputation. The concise summary of the multiple article summaries is as follows: Brand reputation is a crucial aspect of the Science and Technology industry. It encompasses trust, credibility, and public perception of a brand's products and services. Maintaining a strong brand reputation requires consistently delivering high-quality and innovative offerings, as well as effective communication and transparency. Positive brand reputation enhances customer loyalty, attracts investors, and fosters partnerships. However, a negative reputation can lead to decreased sales, loss of trust, and difficulties in the competitive market. Building and safeguarding a reputable brand is essential in the Science and Technology industry.",  # noqa: E501
                    "CEO Reputation": "The reputation of CEOs in the science and technology industry is a crucial aspect that influences their success and the overall perception of their companies. CEOs with positive reputations are seen as trustworthy and capable leaders, leading to increased investor confidence and employee morale. They are also more likely to attract top talent and secure partnerships. However, negative reputations can have detrimental effects, leading to decreased stock prices, difficulty in attracting investors, and even legal consequences. It is important for CEOs in the science and technology industry to prioritize building and maintaining a positive reputation through ethical leadership, transparency, and effective communication.",  # noqa: E501
                    "Customer Response": "The customer response in the science and technology industry is a key aspect that impacts its growth and success. Customers are increasingly demanding personalized experiences and solutions that meet their specific needs. They expect quick and efficient customer service, with prompt responses to their inquiries and concerns. Additionally, customers value transparency and ethical practices from companies in this industry. They are more likely to trust and engage with businesses that prioritize data privacy and security. To stay competitive, companies need to prioritize customer satisfaction and adapt their strategies to meet evolving customer expectations.",  # noqa: E501
                    "Stock Price Impact": "The target industry is Science and Technology, specifically focusing on the impact of stock prices. Summaries from various articles reveal key points in this industry. The stock prices of science and technology companies are influenced by factors such as market trends, financial performance, and technological advancements. Rising demand for innovative products and services, as well as successful research and development efforts, tend to positively affect stock prices. On the other hand, economic downturns, regulatory challenges, and competition can have a negative impact. Overall, stock prices in the science and technology industry are highly sensitive to market dynamics and company-specific factors, making it crucial for investors to carefully assess these variables.",  # noqa: E501
                    "Industry trends": "The science and technology industry is experiencing various trends that are shaping its future. Companies are increasingly focusing on artificial intelligence (AI) and machine learning to enhance their products and services. The integration of AI is seen in various sectors such as healthcare, finance, and manufacturing. Additionally, there is a growing emphasis on sustainability and environmental consciousness, with companies seeking innovative solutions to reduce their carbon footprint. The industry is also witnessing advancements in virtual and augmented reality, enabling immersive experiences and transforming various sectors like gaming, education, and healthcare. Overall, these trends reflect the ever-evolving landscape of science and technology, driving innovation and technological advancements.",  # noqa: E501
                },  # noqa: E501
            },
        },
    }


@pytest.fixture
def test_model_name() -> str:
    """Test model name fixture."""
    return "topic-summarization"


@pytest.fixture
def test_expected_bio_output(test_model_name):
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="topic-summarization",
        attributes={"model_name": "topic-summarization"},
    )
