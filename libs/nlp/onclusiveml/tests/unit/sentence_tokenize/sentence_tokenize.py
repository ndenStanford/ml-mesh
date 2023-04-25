"""sentence tokenize test."""

# Internal libraries
from onclusiveml.nlp.sentence_tokenize import SentenceTokenize


def sentence_tokenize_test():
    text = """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
    The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth."""  # noqa: E501
    tokenizer = SentenceTokenize()
    res = tokenizer.tokenize(content=text)
    assert res["sentences"] == [
        "Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.",  # noqa: E501
        "The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.",  # noqa: E501
    ]
