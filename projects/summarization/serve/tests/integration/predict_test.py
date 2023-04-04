# """Test predict."""

# 3rd party libraries
import pytest


input = (
    """
        Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
        The Tesla Isnc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.
        Musk, 51, has seen his wealth plummet to $137 billion after Tesla shares tumbled in recent weeks, including an 11% drop on Tuesday, according to the Bloomberg Billionaires Index. His fortune peaked at $340 billion on Nov. 4, 2021, and he remained the world's richest person until he was overtaken this month by Bernard Arnault, the French tycoon behind luxury-goods powerhouse LVMH.
        The round-number milestone reflects just how high Musk soared during the run-up in asset prices during the easy-money pandemic era. Tesla exceeded a $1 trillion market capitalization for the first time in October 2021, joining the likes of ubiquitous technology companies Apple Inc., Microsoft Corp., Amazon.com Inc. and Google parent Alphabet Inc., even though its electric vehicles represented only a sliver of the overall auto market.""",  # noqa: E501
)


@pytest.mark.parametrize("input", input)
class TestParametrized:
    def test_turbo(self, test_client, input):
        """Test prediction endpoint."""
        response = test_client.post(
            "/v1/summarization/gpt3/predict",
            json={
                "content": input,
                "max_tokens": 512,
                "desired_length": 100,
                "temperature": 0.7,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            },
        )
        assert len(response.json()["summary"]) > 0
        assert response.json()["model"] == "gpt-3.5-turbo"
        assert response.json()["finish_reason"] == "stop"

    def test_curie(self, test_client, input):
        """Test prediction endpoint."""
        response = test_client.post(
            "/v1/summarization/gpt3/predict",
            json={
                "content": input,
                "max_tokens": 512,
                "desired_length": 100,
                "temperature": 0.7,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "model": "text-curie-001",
            },
        )
        assert len(response.json()["summary"]) > 0
        assert response.json()["model"] == "text-curie-001"
        assert response.json()["finish_reason"] == "stop"

    def test_davinci(self, test_client, input):
        """Test prediction endpoint."""
        response = test_client.post(
            "/v1/summarization/gpt3/predict",
            json={
                "content": input,
                "max_tokens": 512,
                "desired_length": 100,
                "temperature": 0.7,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "model": "text-davinci-003",
            },
        )
        assert len(response.json()["summary"]) > 0
        assert response.json()["model"] == "text-davinci-003"
        assert response.json()["finish_reason"] == "stop"
