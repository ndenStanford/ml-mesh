"""Sentence tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer


def test_tokenize():
    """Test SentenceTokenizer class for tokenizing english text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos. \
The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text)
    assert res["sentences"] == [
        "Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.",  # noqa: E501
        "The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.",  # noqa: E501
    ]


def test_tokenize_fr():
    """Test SentenceTokenizer class for tokenizing French text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud. \
Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne. \
Après le divorce de ses parents en 1979, il continue de vivre avec son père. À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars"""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="fr")
    assert res["sentences"] == [
        "Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud.",
        "Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne.",  # noqa: E501
        "Après le divorce de ses parents en 1979, il continue de vivre avec son père.",
        "À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars",  # noqa: E501
    ]


def test_tokenize_de():
    """Test SentenceTokenizer class for tokenizing German text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos. \
Dem Vorstandsvorsitzenden von Tesla Inc. ist nun ein Novum gelungen: Er ist der einzige Mensch in der Geschichte, der 200 Milliarden US-Dollar aus seinem Nettovermögen gestrichen hat."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="de")
    assert res["sentences"] == [
        "Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos.",  # noqa: E501
        "Dem Vorstandsvorsitzenden von Tesla Inc.",
        "ist nun ein Novum gelungen: Er ist der einzige Mensch in der Geschichte, der 200 Milliarden US-Dollar aus seinem Nettovermögen gestrichen hat.",  # noqa: E501
    ]


def test_tokenize_it():
    """Test SentenceTokenizer class for tokenizing Italian text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos. \
L’amministratore delegato di Tesla Inc. ha ora raggiunto un primato: diventare l’unica persona nella storia a cancellare 200 miliardi di dollari dal proprio patrimonio netto."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="it")
    assert res["sentences"] == [
        "Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos.",  # noqa: E501
        "L’amministratore delegato di Tesla Inc.",
        "ha ora raggiunto un primato: diventare l’unica persona nella storia a cancellare 200 miliardi di dollari dal proprio patrimonio netto.",  # noqa: E501
    ]


def test_tokenize_es():
    """Test SentenceTokenizer class for tokenizing Spanish text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos. \
El director ejecutivo de Tesla Inc. ha logrado ahora una primicia: convertirse en la única persona en la historia en borrar 200.000 millones de dólares de su patrimonio neto."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="es")
    assert res["sentences"] == [
        "Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos.",  # noqa: E501
        "El director ejecutivo de Tesla Inc.",
        "ha logrado ahora una primicia: convertirse en la única persona en la historia en borrar 200.000 millones de dólares de su patrimonio neto.",  # noqa: E501
    ]


def test_tokenize_ca():
    """Test SentenceTokenizer class for tokenizing Catalan text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos. \
El conseller delegat de Tesla Inc. ha aconseguit ara el seu primer: convertir-se en l'única persona de la història que ha esborrat 200.000 milions de dòlars del seu patrimoni net."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["sentences"] == [
        "Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos.",  # noqa: E501
        "El conseller delegat de Tesla Inc. ha aconseguit ara el seu primer: convertir-se en l'única persona de la història que ha esborrat 200.000 milions de dòlars del seu patrimoni net.",  # noqa: E501
    ]


def test_tokenize_ar():
    """Test SentenceTokenizer class for tokenizing Arabic text into a list of sentences.

    Returns:
        None
    """
    text = """إيلون ماسك كان ثاني شخص في التاريخ يجمع ثروة شخصية تزيد عن 200 مليار دولار، حيث وصل إلى هذا الحد في يناير 2021، بعد أشهر من جيف بيزوس. \
الآن، الرئيس التنفيذي لشركة تيسلا قد حقق سابقة خاصة به: أصبح الشخص الوحيد في التاريخ الذي فقد 200 مليار دولار من صافي ثروته."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ar")
    assert res["sentences"] == [
        "إيلون ماسك كان ثاني شخص في التاريخ يجمع ثروة شخصية تزيد عن 200 مليار دولار، حيث وصل إلى هذا الحد في يناير 2021، بعد أشهر من جيف بيزوس.",  # noqa: E501
        "الآن، الرئيس التنفيذي لشركة تيسلا قد حقق سابقة خاصة به: أصبح الشخص الوحيد في التاريخ الذي فقد 200 مليار دولار من صافي ثروته.",  # noqa: E501
    ]


def test_tokenize_zh():
    """Test SentenceTokenizer class for tokenizing Chinese text into a list of sentences.

    Returns:
        None
    """
    text = """埃隆·马斯克是历史上第二个个人财富超过2000亿美元的人，他在2021年1月达到这一门槛，几个月后的杰夫·贝索斯。\
特斯拉公司的首席执行官现在已经实现了他的第一个独特成就：成为历史上唯一一个净资产减少2000亿美元的人。"""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="zh")
    assert res["sentences"] == [
        "埃隆·马斯克是历史上第二个个人财富超过2000亿美元的人，他在2021年1月达到这一门槛，几个月后的杰夫·贝索斯。",
        "特斯拉公司的首席执行官现在已经实现了他的第一个独特成就：成为历史上唯一一个净资产减少2000亿美元的人。",
    ]


def test_tokenize_ko():
    """Test SentenceTokenizer class for tokenizing Korean text into a list of sentences.

    Returns:
        None
    """
    text = """엘론 머스크는 개인 재산이 2000억 달러를 초과하는 두 번째 사람으로, 2021년 1월 제프 베조스에 이어 몇 달 만에 이 기록을 달성했습니다. \
테슬라의 최고경영자(CEO)는 현재 역사상 유일하게 자신의 순자산에서 2000억 달러를 잃은 사람이 되었습니다."""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ko")
    assert res["sentences"] == [
        "엘론 머스크는 개인 재산이 2000억 달러를 초과하는 두 번째 사람으로, 2021년 1월 제프 베조스에 이어 몇 달 만에 이 기록을 달성했습니다.",
        "테슬라의 최고경영자(CEO)는 현재 역사상 유일하게 자신의 순자산에서 2000억 달러를 잃은 사람이 되었습니다.",
    ]


def test_tokenize_ja():
    """Test SentenceTokenizer class for tokenizing Japanese text into a list of sentences.

    Returns:
        None
    """
    text = """イーロン・マスクは、個人の資産が2000億ドルを超えた史上2番目の人物であり、2021年1月にジェフ・ベゾスの数ヶ月後にその閾値を超えました。\
テスラの最高経営責任者は、自らの純資産から2000億ドルを失った史上唯一の人物となりました。"""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ja")
    assert res["sentences"] == [
        "イーロン・マスクは、個人の資産が2000億ドルを超えた史上2番目の人物であり、2021年1月にジェフ・ベゾスの数ヶ月後にその閾値を超えました。",
        "テスラの最高経営責任者は、自らの純資産から2000億ドルを失った史上唯一の人物となりました。",
    ]


def test_tokenize_unknown_language():
    """Test SentenceTokenizer with an unknown language should default to English tokenization."""
    text = """This is a sample English text. It contains multiple sentences."""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="xyz")
    assert res["sentences"] == [
        "This is a sample English text.",
        "It contains multiple sentences.",
    ]


@pytest.mark.parametrize(
    "char",
    SPECIAL_CHARACTERS,
)
def test_tokenize_unique_chars(char):
    """Test SentenceTokenizer class for tokenizing text with unique characters.

    Args:
        char (str): A special character.

    Returns:
        None
    """
    sent1 = "This is sentence one"
    sent2 = "This is sentence two."
    test_sent = sent1 + char + sent2
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=test_sent)
    assert res["sentences"] == [sent1, sent2]
