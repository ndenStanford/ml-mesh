"""Conftest."""

# ML libs
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
# Internal imports
from onclusiveml.models.sentiment import TrainedSentiment


@pytest.fixture(scope="session")
def test_trained_pipeline():
    """Trained pipeline fixture."""
    return pipeline(
        task="sentiment-analysis",
        model="yangheng/deberta-v3-base-absa-v1.1",
    )


@pytest.fixture(scope="session")
def trained_sentiment_instance(test_trained_pipeline):
    """Trained sentiment instance fixture."""
    return TrainedSentiment(trained_sent_pipeline=test_trained_pipeline)


@pytest.fixture
def test_document():
    """Document fixture."""
    return """Steven Paul Jobs (February 24, 1955 - October 5, 2011) was an American business magnate, inventor, and investor.
        He was the co-founder, chairman, and CEO of Apple; the chairman and majority shareholder of Pixar; a member of The Walt Disney Company's board of directors following its acquisition of Pixar; and the founder, chairman, and CEO of NeXT.
        He was a pioneer of the personal computer revolution of the 1970s and 1980s, along with his early business partner and fellow Apple co-founder Steve Wozniak.
        Jobs was born in San Francisco to a Syrian father and German-American mother.
        He was adopted shortly after his birth.
        Jobs attended Reed College in 1972 before withdrawing that same year.
        In 1974, he traveled through India seeking enlightenment before later studying Zen Buddhism.
        He and Wozniak co-founded Apple in 1976 to sell Wozniak's Apple I personal computer.
        Together the duo gained fame and wealth a year later with production and sale of the Apple II, one of the first highly successful mass-produced microcomputers.
        Jobs saw the commercial potential of the Xerox Alto in 1979, which was mouse-driven and had a graphical user interface (GUI).
        This led to the development of the unsuccessful Apple Lisa in 1983, followed by the breakthrough Macintosh in 1984, the first mass-produced computer with a GUI.
        The Macintosh introduced the desktop publishing industry in 1985 with the addition of the Apple LaserWriter, the first laser printer to feature vector graphics.
        In 1985, Jobs departed Apple after a long power struggle with the company's board and its then-CEO, John Sculley.
        That same year, Jobs took a few Apple employees with him to found NeXT, a computer platform development company that specialized in computers for higher-education and business markets.
        In addition, he helped to develop the visual effects industry when he funded the computer graphics division of George Lucas's Lucasfilm in 1986.
        The new company was Pixar, which produced the first 3D computer-animated feature film Toy Story (1995) and went on to become a major animation studio, producing over 27 films since.
        In 1997, Jobs returned to Apple as CEO after the company's acquisition of NeXT.
        He was largely responsible for reviving Apple, which was on the verge of bankruptcy.
        He worked closely with British designer Jony Ive to develop a line of products that had larger cultural ramifications, beginning with the "Think different" advertising campaign and leading to the Apple Store, App Store (iOS), iMac, iPad, iPod, iPhone, iTunes, and iTunes Store.
        In 2001, the original Mac OS was replaced with the completely new Mac OS X (later known as macOS), based on NeXT's NeXTSTEP platform, giving the operating system a modern Unix-based foundation for the first time.
        In 2003, Jobs was diagnosed with a pancreatic neuroendocrine tumor.
        He died of respiratory arrest related to the tumor in 2011, at the age of 56, with Tim Cook succeeding him as CEO of Apple.
        In 2022, he was posthumously awarded the Presidential Medal of Freedom."""  # noqa: E501
