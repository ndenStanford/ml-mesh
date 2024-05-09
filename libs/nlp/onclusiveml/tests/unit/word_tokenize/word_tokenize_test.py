"""Word tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.word import WordTokenizer


def test_word_tokenize():
    """Test word tokenizer."""
    text = """
    Elon Musk was the second person ever to amass a personal fortune of more than $200 billion,
    breaching that threshold in January 2021, months after Jeff Bezos.
    """
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text)
    assert res["words"] == [
        "Elon",
        "Musk",
        "was",
        "the",
        "second",
        "person",
        "ever",
        "to",
        "amass",
        "a",
        "personal",
        "fortune",
        "of",
        "more",
        "than",
        "$",
        "200",
        "billion",
        ",",
        "breaching",
        "that",
        "threshold",
        "in",
        "January",
        "2021",
        ",",
        "months",
        "after",
        "Jeff",
        "Bezos",
        ".",
    ]


def test_word_tokenize_fr():
    """Test word tokenizer French."""
    text = """Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="fr")
    assert res["words"] == [
        "Elon",
        "Reeve",
        "Musk",
        "naît",
        "le",
        "28",
        "juin",
        "1971",
        "à",
        "Pretoria",
        ",",
        "en",
        "Afrique",
        "du",
        "Sud",
        ".",
    ]  # noqa: E501


def test_word_tokenize_de():
    """Test word tokenizer German."""
    text = """Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "war",
        "der",
        "zweite",
        "Mensch",
        "überhaupt",
        ",",
        "der",
        "ein",
        "Privatvermögen",
        "von",
        "mehr",
        "als",
        "200",
        "Milliarden",
        "US-Dollar",
        "anhäufte",
        "und",
        "überschritt",
        "diese",
        "Schwelle",
        "im",
        "Januar",
        "2021",
        ",",
        "Monate",
        "nach",
        "Jeff",
        "Bezos",
        ".",
    ]  # noqa: E501


def test_word_tokenize_it():
    """Test word tokenizer Italian."""
    text = """Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "è",
        "stata",
        "la",
        "seconda",
        "persona",
        "in",
        "assoluto",
        "ad",
        "accumulare",
        "una",
        "fortuna",
        "personale",
        "di",
        "oltre",
        "200",
        "miliardi",
        "di",
        "dollari",
        ",",
        "superando",
        "quella",
        "soglia",
        "nel",
        "gennaio",
        "2021",
        ",",
        "mesi",
        "dopo",
        "Jeff",
        "Bezos",
        ".",
    ]  # noqa: E501


def test_word_tokenize_es():
    """Test word tokenizer Spanish."""
    text = """Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "fue",
        "la",
        "segunda",
        "persona",
        "en",
        "amasar",
        "una",
        "fortuna",
        "personal",
        "de",
        "más",
        "de",
        "200",
        "mil",
        "millones",
        "de",
        "dólares",
        ",",
        "superando",
        "ese",
        "umbral",
        "en",
        "enero",
        "de",
        "2021",
        ",",
        "meses",
        "después",
        "de",
        "Jeff",
        "Bezos",
        ".",
    ]


def test_word_tokenize_ca():
    """Test word tokenizer Catalan."""
    text = """Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "va",
        "ser",
        "la",
        "segona",
        "persona",
        "que",
        "va",
        "acumular",
        "una",
        "fortuna",
        "personal",
        "de",
        "més",
        "de",
        "200.000",
        "milions",
        "de",
        "dòlars",
        ",",
        "superant",
        "aquest",
        "llindar",
        "el",
        "gener",
        "del",
        "2021",
        ",",
        "mesos",
        "després",
        "de",
        "Jeff",
        "Bezos",
        ".",
    ]  # noqa: E501


def test_word_tokenize_zh():
    """Test word tokenizer Chinese."""
    text = """埃隆·马斯克是有史以来第二位个人财富超过2000亿美元的人，他于2021年1月突破这一门槛，比杰夫·贝佐斯晚了几个月。"""
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="zh")
    assert res["words"] == [
        "埃隆",
        "·",
        "马斯克",
        "是",
        "有史以来",
        "第二位",
        "个人",
        "财富",
        "超过",
        "2000",
        "亿美元",
        "的",
        "人",
        "，",
        "他于",
        "2021",
        "年",
        "1",
        "月",
        "突破",
        "这一",
        "门槛",
        "，",
        "比",
        "杰夫",
        "·",
        "贝佐斯晚",
        "了",
        "几个",
        "月",
        "。",
    ]


def test_word_tokenize_ja():
    """Test word tokenizer Japanese."""
    text = """イーロン・マスクは、2021年1月に閾値を突破した、個人の財産が2000億ドルを超える2番目の人物であり、ジェフ・ベゾスの数か月後でした。"""
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ja")
    assert res["words"] == [
        "イーロン・マスク",
        "は",
        "、",
        "2021",
        "年",
        "1",
        "月",
        "に",
        "閾値",
        "を",
        "突破",
        "し",
        "た",
        "、",
        "個人",
        "の",
        "財産",
        "が",
        "2000",
        "億",
        "ドル",
        "を",
        "超える",
        "2",
        "番目",
        "の",
        "人物",
        "で",
        "あり",
        "、",
        "ジェフ",
        "・",
        "ベゾス",
        "の",
        "数",
        "か月",
        "後",
        "でし",
        "た",
        "。",
    ]


def test_word_tokenize_ko():
    """Test word tokenizer Korean."""
    text = "일론 머스크는 2021년 1월에 2000억 달러 이상의 개인 재산을 축적한 두 번째 사람이었으며,그는 제프 베조스 몇 달 후에 이 기준을 넘었습니다."
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ko")
    assert res["words"] == [
        "일론",
        "머스크는",
        "2021년",
        "1월에",
        "2000억",
        "달러",
        "이상의",
        "개인",
        "재산을",
        "축적한",
        "두",
        "번째",
        "사람이었으며",
        ",",
        "그는",
        "제프",
        "베조스",
        "몇",
        "달",
        "후에",
        "이",
        "기준을",
        "넘었습니다",
        ".",
    ]


def test_word_tokenize_ar():
    """Test word tokenizer Arabic."""
    text = "الطقس جميل اليوم في المدينة"
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="arabic")
    assert res["words"] == ["الطقس", "جميل", "اليوم", "في", "المدينة"]


@pytest.mark.parametrize(
    "char",
    SPECIAL_CHARACTERS,
)
def test_word_tokenize_unique_chars(char):
    """Test word tokenizer on unique characters."""
    word1 = "one"
    word2 = "two"
    test_word = word1 + char + word2
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=test_word)
    assert res["words"] == [word1, word2]
